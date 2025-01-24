from sqlalchemy import select

from data.models import Fund, Round
from pre_award.db import db


def get_fund_and_round(fund_short_name: str, round_short_name: str) -> tuple[Fund, Round]:
    fund: Fund = db.session.scalars(select(Fund).where(Fund.short_name == fund_short_name.upper())).one_or_none()
    if fund:
        round: Round = db.session.scalars(
            select(Round)
            .where(Round.short_name == round_short_name.upper())
            .where(Round.fund_id == fund.id)
            .where(Round.is_not_yet_open.is_(False))
        ).one_or_none()
        return fund, round
    return None, None
