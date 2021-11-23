from stabibot import settings, telegram
from stabibot.format import format_message
from stabibot.shifts import get_gaps


def run():
    gaps = get_gaps(min_persons=settings.MIN_PERSONS)
    if gaps:
        message = format_message(gaps)
        telegram.send_message(message)


run()
