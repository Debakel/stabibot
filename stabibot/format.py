
from datetime import datetime

import pendulum
from pendulum import DateTime


def format_time(dt: DateTime) -> str:
    return dt.in_timezone('Europe/Berlin').format("HH:mm", locale="de")


def format_from_date(dt: datetime) -> str:
    """Gibt `Heute 12:00`, `Morgen 17:00` oder `Freitag 09:00` zurück
    """
    dt = pendulum.instance(dt)

    if dt.date() == pendulum.today().date():
        day = "Heute"
    elif dt.date() == pendulum.tomorrow().date():
        day = "Morgen"
    else:
        day = dt.format("dddd", locale="de")

    hour = format_time(dt)

    return f"{day} {hour}"


