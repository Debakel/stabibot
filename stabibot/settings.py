import os

import pytz
from dotenv import load_dotenv

load_dotenv()

ICS_FEED = os.environ.get("ICS_FEED")
TIME_ZONE = pytz.timezone("Europe/Berlin")
RESOLUTION_MINUTES = 1
DEFAULT_RANGE_HOURS = 24
MIN_PERSONS = 2