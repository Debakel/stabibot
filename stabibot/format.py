"""Modul zum Formatieren der Telegramnachrichten.

Beispielnachricht:

    ☝️ Folgende Schichten sind noch nicht vergeben:

    ➡️ Morgen 09:00 bis 09:45
    ➡️ Morgen 10:00 bis 11:00
    ➡️ Donnerstag 09:00 bis 10:45

    Hier kannst du dich dafür eintragen: https://example.org/plan

    LG Stabine ❤️
"""

from datetime import datetime
from typing import List

import pendulum

from stabibot import settings
from stabibot.intervals import Interval


def format_from_date(dt: datetime) -> str:
    dt = pendulum.instance(dt)

    if dt.date() == pendulum.today().date():
        day = "Heute"
    elif dt.date() == pendulum.tomorrow().date():
        day = "Morgen"
    else:
        day = dt.format("dddd", locale="de")

    hour = dt.format("HH:mm", locale="de")

    return f"{day} {hour}"


def format_to_date(dt: datetime) -> str:
    dt = pendulum.instance(dt)
    return dt.format("HH:mm")


def format_message(gaps: List[Interval]) -> str:
    slots = []
    for gap in gaps:
        start = format_from_date(gap.start_datetime)
        end = format_to_date(gap.end_datetime)
        msg = f"➡️ {start} bis {end}"
        slots.append(msg)

    slots = "\n".join(slots)

    message = f"""
☝️ Folgende Schichten sind noch nicht vergeben:
   
{slots}

Hier kannst du dich dafür eintragen: {settings.SCHICHTPLAN_URL}

LG Stabine ❤️
    """
    return message
