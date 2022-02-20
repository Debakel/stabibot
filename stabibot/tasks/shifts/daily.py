from stabibot import settings, telegram
from stabibot.tasks.shifts.format import format_message
from stabibot.shifts import Calendar


def run():
    gaps = Calendar(settings.ICS_FEED).get_gaps(min_persons=settings.MIN_PERSONS)
    if gaps:
        message = format_message(gaps)
        telegram.send_message(message)


run()
