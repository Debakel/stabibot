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
from pendulum import DateTime, Duration

from stabibot import settings
from stabibot.intervals import Interval


def format_time(dt: DateTime) -> str:
    return dt.format("HH:mm", locale="de")


def format_from_date(dt: datetime) -> str:
    dt = pendulum.instance(dt)

    if dt.date() == pendulum.today().date():
        day = "Heute"
    elif dt.date() == pendulum.tomorrow().date():
        day = "Morgen"
    else:
        day = dt.format("dddd", locale="de")

    hour = format_time(dt)

    return f"{day} {hour}"


def format_message(gaps: List[Interval]) -> str:
    slots = []
    for gap in gaps:
        start = format_from_date(gap.start_datetime)
        end = format_time(pendulum.instance(gap.start_datetime))
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


def format_alarm_message_slot(gap: Interval) -> str:
    start = format_time(pendulum.instance(gap.start_datetime))
    end = format_time(pendulum.instance(gap.end_datetime))

    return f"➡️ {start} - {end}"


def format_alarm_message(gaps: List[Interval]) -> str:
    instabil_ab = pendulum.instance(gaps[0].start_datetime)
    now = pendulum.now()

    time_remaining = (instabil_ab - now).as_interval()
    if time_remaining.hours >= 1:
        time_remaining = Duration(hours=time_remaining.hours)
    else:
        time_remaining = Duration(minutes=time_remaining.total_minutes())

    time_remaining = time_remaining.in_words("de")

    slots = "\n".join([format_alarm_message_slot(gap) for gap in gaps])

    return f"""
🆘 In {time_remaining} ist das Camp instabil 🆘 
🆘 Es gibt folgende Lücken im Schichtplan:

{slots}
    
Kannst du spontan vorbeikommen oder bist schon da? 
Dann trage dich hier ein: {settings.SCHICHTPLAN_URL}

Eure Stabine ❤️
    """
