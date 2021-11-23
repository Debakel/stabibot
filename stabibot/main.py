from stabibot import telegram, settings
from stabibot.shifts import get_gaps
from stabibot.format import format_message


def run():
    gaps = get_gaps(min_persons=settings.MIN_PERSONS)
    message = format_message(gaps)
    telegram.send_message(message)


run()
