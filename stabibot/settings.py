import os

import pytz
from dotenv import load_dotenv

load_dotenv()

SCHICHTPLAN_URL = os.environ.get("SCHICHTPLAN_URL")
ICS_FEED = os.environ.get("ICS_FEED")
TIME_ZONE = pytz.timezone(os.environ.get("TZ", "Europe/Berlin"))
RESOLUTION_MINUTES = 1

# Wie viele Stunden in die Zukunft sollen überprüft werden?
DEFAULT_RANGE_HOURS = int(os.environ.get("DEFAULT_RANGE_HOURS", 36))
ALARM_RANGE_HOURS = int(os.environ.get("ALARM_RANGE_HOURS", 3))

# Wie viel Personen müssen gleichzeitig anwesend sein?
MIN_PERSONS = 2

TELEGRAM_AUTH_TOKEN = os.environ.get("TELEGRAM_AUTH_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
