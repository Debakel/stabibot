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

from stabibot import settings
from stabibot.intervals import Interval, IntervalCollection
from stabibot.settings import (
    TIME_ZONE,
    RESOLUTION_MINUTES,
    DEFAULT_RANGE_HOURS,
)


def get_schichten(interval: Interval) -> List[Interval]:
    """Gibt im Kalendar eingetragene Schichten innerhalb des übergebenen Zeitraums zurück"""
    ical_string = requests.get(settings.ICS_FEED).text

    calendar = icalendar.Calendar.from_ical(ical_string)

    # Package `recurring_ical_events` can not handle timezone aware datetime objects.
    # Workaround:
    # 1. Convert to UTC
    # 2. Remove timezone info
    #
    # See https://github.com/niccokunzmann/python-recurring-ical-events/issues/52
    start = interval.start_datetime.astimezone(pytz.UTC).replace(tzinfo=None)
    end = interval.end_datetime.astimezone(pytz.UTC).replace(tzinfo=None)

    events = recurring_ical_events.of(calendar).between(start, end)

    # Entferne "Repro-Schichten"
    events = [event for event in events if not "Repro" in event.get("SUMMARY", "")]

    schichten = list()
    for event in events:
        start = event["DTSTART"].dt
        end = event["DTEND"].dt

        if type(start) == date:
            start = datetime.combine(start, datetime.min.time())
        if type(end) == date:
            end = datetime.combine(end, datetime.min.time())

        if not start.tzinfo:
            start = TIME_ZONE.localize(start)
        if not end.tzinfo:
            end = TIME_ZONE.localize(end)

        schichten.append(Interval(start, end))

    schichten = sorted(schichten, key=lambda schicht: schicht.start_datetime)

    return schichten


def get_gaps(
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

    schichten = IntervalCollection(get_schichten(timerange))
    gaps = IntervalCollection()

    for slot in timerange.slots(timedelta(minutes=RESOLUTION_MINUTES)):
        num_attendees = schichten.count_intersections(slot)

        if num_attendees < min_persons:
            gaps.add_or_join(slot)

    return gaps.intervals
