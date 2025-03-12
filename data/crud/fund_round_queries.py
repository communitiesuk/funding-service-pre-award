from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import contains_eager

from data.models import Fund, Round
from pre_award.db import db


def get_fund(fund_short_name: str) -> Fund | None:
    return db.session.scalar(select(Fund).where(Fund.short_name == fund_short_name))


def get_funds_with_rounds() -> Sequence[Fund]:
    return db.session.scalars(select(Fund).join(Fund.rounds).options(contains_eager(Fund.rounds))).unique().all()


def get_round(fund_short_name: str, round_short_name: str) -> Round | None:
    round = db.session.scalar(
        select(Round)
        .join(Fund)
        .options(contains_eager(Round.fund))
        .where(Fund.short_name == fund_short_name)
        .where(Round.short_name == round_short_name)
        .where(Round.is_not_yet_open.is_(False))
    )
    return round


def get_rounds_for_application_deadline_reminders() -> Sequence[Round]:
    """
    Retrieve rounds that are eligible for sending application deadline reminder emails "now".

    `round.reminder_date` and `round.deadline` are naive timestamps in Europe/London local time. `func.now()` by
    default returns a UTC timestamp from postgres, so in order to do a correct comparison we need to tell postgres
    that the reminder_date is actually in the europe/london timezone.
    """
    return db.session.scalars(
        select(Round)
        .join(Round.fund)
        .where(
            Round.application_reminder_sent.is_(False),
            func.timezone("Europe/London", Round.reminder_date) <= func.now(),
            func.timezone("Europe/London", Round.deadline) > func.now(),
        )
    ).all()


def set_application_reminder_sent(round: Round) -> None:
    round.application_reminder_sent = True
    db.session.commit()
