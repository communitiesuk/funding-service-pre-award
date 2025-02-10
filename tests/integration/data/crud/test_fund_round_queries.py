from datetime import datetime

import pytest

from data.crud.fund_round_queries import get_rounds_for_application_deadline_reminders
from tests.integration.seeding import seed_fund, seed_round


@pytest.mark.parametrize(
    "now_utc, reminder_date, deadline, reminder_sent, should_find",
    (
        # Current time is before reminder date - skip
        (datetime(2020, 1, 2, 9, 59), datetime(2020, 1, 2, 10), datetime(2020, 1, 3), False, False),
        # Current time is >= reminder date - take
        (datetime(2020, 1, 2, 10), datetime(2020, 1, 2, 10), datetime(2020, 1, 3), False, True),
        # Current time is >= reminder date, but reminders have already been sent - skip
        (datetime(2020, 1, 2, 10), datetime(2020, 1, 2, 10), datetime(2020, 1, 3), True, False),
        # Current time is < deadline - take
        (datetime(2020, 1, 2, 23, 59, 59), datetime(2020, 1, 2, 10), datetime(2020, 1, 3), False, True),
        # Current time is < deadline, but reminders have already been sent - skip
        (datetime(2020, 1, 2, 23, 59, 59), datetime(2020, 1, 2, 10), datetime(2020, 1, 3), True, False),
        # Current time is >= deadline - skip
        (datetime(2020, 1, 3, 0, 0, 0), datetime(2020, 1, 2, 10), datetime(2020, 1, 3), False, False),
        #
        # 8am UTC in summer months is 9am BST. reminder dates are in BST (but stored without tzinfo)
        (datetime(2020, 6, 1, 8, 0, 0), datetime(2020, 6, 1, 9, 0, 0), datetime(2020, 6, 2), False, True),
        (datetime(2020, 6, 1, 8, 0, 0), datetime(2020, 6, 1, 9, 0, 1), datetime(2020, 6, 2), False, False),
    ),
)
def test_get_rounds_for_application_deadline_reminders(
    app, session, mocker, now_utc, reminder_date, deadline, reminder_sent, should_find
):
    seed_round(
        session,
        seed_fund(session),
        reminder_date=reminder_date,
        deadline=deadline,
        application_reminder_sent=reminder_sent,
    )

    mock_now = mocker.patch("sqlalchemy.func.now")
    mock_now.return_value = now_utc

    rounds = get_rounds_for_application_deadline_reminders()

    if should_find:
        assert rounds
    else:
        assert not rounds
