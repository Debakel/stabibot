from stabibot import telegram
from stabibot.shifts import get_gaps
from stabibot.format import format_message


def run():
    gaps = get_gaps()
    message = format_message(gaps)
    telegram.send_message(message)

run()
