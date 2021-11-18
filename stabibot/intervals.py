from datetime import timedelta
from typing import List

from datetimerange import DateTimeRange


class Interval(DateTimeRange):
    """Ein Zeitintervall."""

    def slots(self, size: timedelta):
        """Zerlegt das Zeitintervall in Teilstücke"""
        duration = self.end_datetime - self.start_datetime

        slot_num = int(duration / size)

        slots: List[Interval] = [
            Interval(
                self.start_datetime + size * X, self.start_datetime + size * (X + 1)
            )
            for X in range(slot_num)
        ]

        return slots


class IntervalCollection:
    intervals: List[Interval] = []

    def __init__(self, entries: List[Interval] = None):
        if not entries:
            entries = list()
        self.intervals = entries

    def add_or_join(self, new_interval: Interval):
        """Fügt das neue Intervall der Sammlung hinzu

        Falls das neue Intervall sich mit einem bestehenden überschneidet, wird das bestehende stattdessen erweitert.
        """
        for interval in self.intervals:
            if interval.is_intersection(new_interval):
                new_interval = interval.encompass(new_interval)
                self.intervals.remove(interval)

        self.intervals.append(new_interval)

        self.intervals = sorted(self.intervals, key=lambda i: i.start_datetime)

    def count_intersections(self, interval: Interval) -> int:
        """Zählt, wie viele der Einträge der Collection sich mit `interval` überschneiden"""
        count = 0
        for schicht in self.intervals:
            if schicht.is_intersection(interval):
                count += 1

        return count
