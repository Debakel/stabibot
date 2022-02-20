import pytz
from environs import Env

env = Env()
env.read_env()

SCHICHTPLAN_URL = env.str("SCHICHTPLAN_URL")
ICS_FEED = env("ICS_FEED")
TIME_ZONE = pytz.timezone(env.str("TZ", "Europe/Berlin"))
RESOLUTION_MINUTES = 1

# Wie viele Stunden in die Zukunft sollen überprüft werden?
DEFAULT_RANGE_HOURS = env.int("DEFAULT_RANGE_HOURS", 36)
ALARM_RANGE_HOURS = env.int("ALARM_RANGE_HOURS", 3)

# Wie viel Personen müssen gleichzeitig anwesend sein?
MIN_PERSONS = 2

TELEGRAM_AUTH_TOKEN = env.str("TELEGRAM_AUTH_TOKEN")
TELEGRAM_CHAT_ID = env.str("TELEGRAM_CHAT_ID")
