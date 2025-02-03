from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from data.models import Fund, Round
from pre_award.db import db


def get_fund(fund_short_name: str) -> Fund | None:
    return db.session.scalar(select(Fund).where(Fund.short_name == fund_short_name.upper()))


def get_round(fund_short_name: str, round_short_name: str) -> Round | None:
    round = db.session.scalar(
        select(Round)
        .join(Fund)
        .options(contains_eager(Round.fund))
        .where(Fund.short_name == fund_short_name.upper())
        .where(Round.short_name == round_short_name.upper())
        .where(Round.is_not_yet_open.is_(False))
    )
    return round
