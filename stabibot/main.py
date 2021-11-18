from typing import List

from stabibot import telegram
from stabibot.calendar import get_gaps
from stabibot.intervals import Interval


def format_message(gaps: List[Interval]):
    message = f"""Es fehlen noch folgende Schichten: {gaps}"""
    return message


def run():
    gaps = get_gaps()
    message = format_message(gaps)
    telegram.send_message(message)


run()
