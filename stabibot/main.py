import locale
from string import Template
from typing import List

from stabibot import telegram
from stabibot.calendar import get_gaps
from stabibot.intervals import Interval

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

gap_template = Template('')


def format_message(gaps: List[Interval]):
    x = [f"➡️ {gap.start_datetime.strftime('%A %H:%M')} bis {gap.end_datetime.strftime('%H:%M')}" for gap in gaps]
    x = "\n".join(x)
    message = f"""
☝️
Folgende Schichten sind noch nicht vergeben:
   
{x}

Hier kannst du dich dafür eintragen: https://teamup.com/ks4o76civjv5vxqjr7

LG Stabine ❤️
    """
    return message


def run():
    gaps = get_gaps()
    message = format_message(gaps)
    telegram.send_message(message)


run()
