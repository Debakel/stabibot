from typing import List

import pendulum

from stabibot import settings
from stabibot.intervals import Interval


def format_message(gaps: List[Interval]) -> str:
    slots = []
    for gap in gaps:
        start = pendulum.instance(gap.start_datetime)
        end = pendulum.instance(gap.end_datetime)
        msg = f"➡️ {start.format('dddd HH:mm', locale='de')} bis {end.format('HH:mm', locale='de')}"
        slots.append(msg)

    slots = '\n'.join(slots)

    message = f"""
☝️
Folgende Schichten sind noch nicht vergeben:
   
{slots}

Hier kannst du dich dafür eintragen: {settings.SCHICHTPLAN_URL}

LG Stabine ❤️
    """
    return message