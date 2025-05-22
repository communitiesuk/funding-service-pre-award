from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def get_now_from_utc_time_without_tzinfo() -> datetime:
    """
    Returns the current date and time, using UTC, but without timezone info so it can be compared
    to a date from the db.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


def get_now_UK_time_without_tzinfo() -> datetime:
    """
    Returns the current date and time, using London time, but without timezone info so it can be compared
    to a date from the db.
    """
    return get_now_from_utc_time_without_tzinfo().astimezone(ZoneInfo("Europe/London")).replace(tzinfo=None)
