"""Schickt Erinnerung ein Tag vorm Plenum.
"""
from stabibot import telegram
from stabibot.format import format_from_date
from stabibot.intervals import Interval
from stabibot.settings import TELEGRAM_CHAT_ID
from stabibot.shifts import Event
from stabibot.tasks.plenum import get_plenaries, TOPS_URL


def format_message(plenum: Event):
    return f"""
🥳 <b>Reminder:</b> {format_from_date(plenum.start)} ist {plenum.summary}!
            
➡️ Zu den TOPs: {TOPS_URL}
"""


for plenum in get_plenaries(interval=Interval.from_now(hours=28)):
    telegram.send_message(format_message(plenum), chat_id=TELEGRAM_CHAT_ID)
