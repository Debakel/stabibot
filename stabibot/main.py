from typing import List

import pendulum

from stabibot import telegram
from stabibot.calendar import get_gaps
from stabibot.intervals import Interval


def format_message(gaps: List[Interval]):
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

Hier kannst du dich dafür eintragen: https://teamup.com/ks4o76civjv5vxqjr7

LG Stabine ❤️
    """
    return message


def run():
    gaps = get_gaps()
    message = format_message(gaps)
    telegram.send_message(message)


run()
