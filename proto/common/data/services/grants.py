from datetime import date

from sqlalchemy import select

from db import db
from proto.common.data.models.fund import Fund
from proto.common.data.models.round import Round


def get_grant(short_code: str):
    grant = db.session.scalars(select(Fund).filter(Fund.short_name == short_code)).one()
    return grant


def get_active_round(grant_short_code: str):
    round = db.session.scalars(
        select(Round)
        .join(Fund)
        .filter(
            Fund.short_name == grant_short_code,
            # probably want some way of having rounds that are always open especially for uncompeted grants
            # note you might want to show funds that have been live in the past - they want to be able to log in?
            Round.proto_start_date <= date.today(),
            Round.proto_end_date >= date.today(),
        )
    ).one_or_none()
    return round, round.proto_grant if round else None
