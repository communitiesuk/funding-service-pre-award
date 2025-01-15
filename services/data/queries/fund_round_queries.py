from sqlalchemy import select

from pre_award.db import db
from services.data.models.fund import Fund
from services.data.models.round import Round


def get_fund_and_round(fund_short_name: str, round_short_name: str) -> tuple[Fund, Round]:
    fund: Fund = db.session.scalars(select(Fund).where(Fund.short_name == fund_short_name.upper())).one_or_none()
    if fund:
        round: Round = db.session.scalars(
            select(Round)
            .where(Round.short_name == round_short_name.upper())
            .where(Round.fund_id == fund.id)
            .where(Round.is_not_yet_open == False)  # noqa: E712
        ).one_or_none()
        return fund, round
    return None, None
