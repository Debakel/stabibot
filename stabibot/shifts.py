"""
Z = Zeitraum, der überprüft werden soll
N = So viele Menschen müssen zu jedem Zeitpunkt anwesend sein

Prozedere:

1. Zerlege Z in Teilstücke von je X Minuten
2. Überprüfe für jedes Teilstück, ob weniger als N Menschen anwesend sind

"""
from datetime import datetime, timedelta, date
from typing import List

import icalendar
import pytz
import recurring_ical_events
import requests
from pydantic import BaseModel, Field, validator

from stabibot.intervals import Interval, IntervalCollection
from stabibot.settings import (
    TIME_ZONE,
    RESOLUTION_MINUTES,
    DEFAULT_RANGE_HOURS,
)


class Event(BaseModel):
    summary: str = Field(alias="SUMMARY")
    start: datetime = Field(alias="DTSTART")
    end: datetime = Field(alias="DTEND")

    @validator('start', 'end', pre=True)
    def validate_start(cls, value):
        value = value.dt
        if type(value) == date:
            value = datetime.combine(value, datetime.min.time())
        if not value.tzinfo:
            value = TIME_ZONE.localize(value)
        return value


class Calendar:
    def __init__(self, ics_feed: str):
        self.ics_feed = ics_feed

    @property
    def _calendar(self):
        content = requests.get(self.ics_feed).text
        return icalendar.Calendar.from_ical(content)

    def get_within(self, interval: Interval) -> List[Event]:
        """Gibt alle Events im gewählten Zeitintervall zurück
        """

        # Package `recurring_ical_events` can not handle timezone aware datetime objects.
        # Workaround:
        #   1. Convert to UTC
        #   2. Remove timezone info
        #
        # See https://github.com/niccokunzmann/python-recurring-ical-events/issues/52
        start = interval.start_datetime.astimezone(pytz.UTC).replace(tzinfo=None)
        end = interval.end_datetime.astimezone(pytz.UTC).replace(tzinfo=None)

        events = recurring_ical_events.of(self._calendar).between(start, end)

        events = [Event.parse_obj(event) for event in events]

        return events

    def get_schichten(self, interval: Interval) -> List[Interval]:
        """Gibt im Kalendar eingetragene Schichten innerhalb des übergebenen Zeitraums zurück"""
        events = self.get_within(interval)

        # Entferne "Repro-Schichten"
        events = [event for event in events if not "Repro" in event.summary]

        schichten = [Interval(event.start, event.end) for event in events]
        schichten = sorted(schichten, key=lambda schicht: schicht.start_datetime)

        return schichten

    def get_gaps(self,
                 min_persons: int, start_date: datetime = None, end_date: datetime = None
                 ) -> List[Interval]:
        """Gibt Lücken im Schichtplan zurück, die im angegebenen Zeitintervall liegen

        :param min_persons: Anzahl Personen, die immer anwesend sein müssen
        """
        if not start_date:
            start_date = datetime.now(tz=pytz.timezone("Europe/Berlin"))
        if not end_date:
            end_date = start_date + timedelta(hours=DEFAULT_RANGE_HOURS)

        timerange = Interval(start_date, end_date)

        schichten = IntervalCollection(self.get_schichten(timerange))
        gaps = IntervalCollection()

        for slot in timerange.slots(timedelta(minutes=RESOLUTION_MINUTES)):
            num_attendees = schichten.count_intersections(slot)

            if num_attendees < min_persons:
                gaps.add_or_join(slot)

        return gaps.intervals
