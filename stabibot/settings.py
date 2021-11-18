import os

import pytz
from dotenv import load_dotenv

load_dotenv()

ICS_FEED = os.environ.get("ICS_FEED")
TIME_ZONE = pytz.timezone("Europe/Berlin")
RESOLUTION_MINUTES = 1
DEFAULT_RANGE_HOURS = 36
MIN_PERSONS = 2

TELEGRAM_AUTH_TOKEN = os.environ.get("TELEGRAM_AUTH_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
