from datetime import datetime, timedelta

from stabibot import settings, telegram
from stabibot.format import format_alarm_message
from stabibot.shifts import get_gaps


def alarm():
    gaps = get_gaps(
        min_persons=settings.MIN_PERSONS,
        end_date=datetime.now(tz=settings.TIME_ZONE) + timedelta(hours=settings.ALARM_RANGE_HOURS),
    )
    if gaps:
        message = format_alarm_message(gaps)
        telegram.send_message(message)


alarm()
