import os
from datetime import datetime
from zoneinfo import ZoneInfo

from common.utils.date_time_utils import get_now_UK_time_without_tzinfo


def test_get_now_uk_time_without_tzinfo_is_correct_regardless_of_system_timezone(monkeypatch):
    """
    Regression test: the previous implementation built a naive UTC datetime and called .astimezone()
    on it, which Python interprets using the process's own system-local timezone - silently wrong
    whenever that isn't UTC. Force a non-UTC system timezone here to prove the fix doesn't regress.
    """
    monkeypatch.setenv("TZ", "America/New_York")
    if hasattr(os, "tzset"):
        os.tzset()
    try:
        result = get_now_UK_time_without_tzinfo()
        expected = datetime.now(ZoneInfo("Europe/London")).replace(tzinfo=None)
    finally:
        monkeypatch.delenv("TZ", raising=False)
        if hasattr(os, "tzset"):
            os.tzset()
    # The result and expected calls are independent so will be a few milliseconds apart - but 5s is close enough
    # to catch obvious errors which would result in buggy timezone offsets
    assert abs((result - expected).total_seconds()) < 5
