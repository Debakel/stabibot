from typing import List

from stabibot.intervals import Interval
from stabibot.settings import env, ICS_FEED
from stabibot.shifts import Event, Calendar

VIDEOCALL_URL = env("PLENARY_VIDEOCALL_URL")
TOPS_URL = env("PLENARY_TOPS_URL")


def get_plenaries(interval: Interval) -> List[Event]:
    events = Calendar(ics_feed=ICS_FEED).get_within(interval)
    return [event for event in events if 'plenum' in event.summary.lower()]
