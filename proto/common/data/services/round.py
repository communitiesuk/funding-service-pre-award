from datetime import date

import psycopg2
import sqlalchemy
from flask_babel import lazy_gettext as _l
from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from db import db
from proto.common.data.exceptions import DataValidationError
from proto.common.data.models import Fund, Round
from proto.common.data.models.fund import FundStatus


def create_round(fund_id):
    existing_rounds = db.session.scalars(select(Round).join(Round.proto_grant).filter(Fund.id == fund_id)).all()
    round_id = str(len(existing_rounds) + 1)
    code = "R" + round_id
    name = f"Round {round_id}"

    round = Round(
        short_name=code,
        title_json={"en": name, "cy": name},
        opens=None,
        deadline=None,
        proto_start_date=None,
        proto_end_date=None,
        prospectus="",
        privacy_notice="",
        support_times="",
        support_days="",
        project_name_field_id="",
        fund_id=fund_id,
    )
    db.session.add(round)

    try:
        db.session.commit()  # TODO: plan for transaction management

    except sqlalchemy.exc.IntegrityError as e:
        cause = e.__cause__
        if isinstance(cause, psycopg2.errors.UniqueViolation) and "Key (short_name)=" in cause.diag.message_detail:
            raise DataValidationError(
                message=_l(f"A round with the code ‘{code}’ already exists. Enter a different code."),
                schema_field_name="code",
            ) from e

    return round


def update_round(round: Round, draft: bool | None = None):
    if draft is not None:
        round.proto_draft = draft

    db.session.add(round)

    db.session.commit()


def get_open_rounds():
    return (
        db.session.scalars(
            select(Round)
            .join(Fund, Fund.id == Round.fund_id)
            .options(contains_eager(Round.proto_grant))
            .filter(
                Fund.proto_status == FundStatus.LIVE,
                Round.proto_draft.is_(False),
                # probably want some way of having rounds that are always open especially for uncompeted grants
                Round.proto_start_date <= date.today(),
                Round.proto_end_date >= date.today(),
            )
        )
        .unique()
        .all()
    )
