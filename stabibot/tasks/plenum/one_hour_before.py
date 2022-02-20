"""Schickt Erinnerung eine Stunde vorm Plenum
"""
from stabibot import telegram
from stabibot.format import format_from_date
from stabibot.intervals import Interval
from stabibot.settings import TELEGRAM_CHAT_ID
from stabibot.shifts import Event
from stabibot.tasks.plenum import VIDEOCALL_URL, TOPS_URL, get_plenaries


def format_message(plenum: Event):
    return f"""
🥁 Plenum! Ple-e-e-num! Ple- es ist Ple- es ist Ple- es ist Ple- es ist Ple- es ist Ple-e-e-num!

{format_from_date(plenum.start)} ist {plenum.summary}!

➡️ Falls online, dann hier: {VIDEOCALL_URL}
➡️ Zu den TOPs: {TOPS_URL}
"""


for plenum in get_plenaries(Interval.from_now(hours=1.5)):
    telegram.send_message(format_message(plenum), chat_id=TELEGRAM_CHAT_ID)
