from datetime import date

import psycopg2
import sqlalchemy.exc
from flask_babel import lazy_gettext as _l
from sqlalchemy import select
from sqlalchemy.orm import contains_eager, joinedload

from db import db
from proto.common.data.exceptions import DataValidationError
from proto.common.data.models import ProtoReportingRound
from proto.common.data.models.fund import Fund, FundStatus
from proto.common.data.models.round import Round


def get_grant(short_code: str):
    grant = db.session.scalars(select(Fund).filter(Fund.short_name == short_code)).one()
    return grant


def get_grant_and_round(grant_code: str, round_code: str) -> tuple[Fund, Round]:
    round = (
        db.session.scalars(
            select(Round).join(Fund).filter(Fund.short_name == grant_code, Round.short_name == round_code)
        )
        .unique()
        .one()
    )
    return round.proto_grant, round


def get_grant_and_reporting_round(grant_code: str, round_ext_id: str) -> tuple[Fund, Round]:
    round = (
        db.session.scalars(
            select(ProtoReportingRound)
            .join(Fund)
            .filter(Fund.short_name == grant_code, ProtoReportingRound.external_id == round_ext_id)
        )
        .unique()
        .one()
    )
    return round.grant, round


def get_active_round(grant_short_code: str):
    round = db.session.scalar(
        select(Round)
        .join(Round.proto_grant)
        .options(contains_eager(Round.proto_grant))
        .filter(
            Fund.short_name == grant_short_code,
            Round.proto_draft.is_(False),
            # probably want some way of having rounds that are always open especially for uncompeted grants
            Round.proto_start_date <= date.today(),
            Round.proto_end_date >= date.today(),
        )
    )
    return round, round.proto_grant if round else None


def get_all_grants_with_rounds():
    return db.session.scalars(select(Fund).options(joinedload(Fund.rounds))).unique().all()


def create_grant(
    name,
    funding_type,
):
    code = "".join([word[0] for word in name.upper().split(" ")])
    grant = Fund(
        name_json={"en": name, "cy": ""},
        title_json={"en": "", "cy": ""},
        short_name=code,
        description_json={"en": "", "cy": ""},
        owner_organisation_name="",
        owner_organisation_shortname="",
        owner_organisation_logo_uri="",
        funding_type=funding_type,
        welsh_available=False,
        ggis_scheme_reference_number="",
        proto_name=name,
    )
    db.session.add(grant)

    try:
        db.session.commit()  # TODO: plan for transaction management

    except sqlalchemy.exc.IntegrityError as e:
        cause = e.__cause__
        if isinstance(cause, psycopg2.errors.UniqueViolation) and "Key (short_name)=" in cause.diag.message_detail:
            raise DataValidationError(
                message=_l(f"A grant with the code ‘{code}’ already exists. Enter a different code."),
                schema_field_name="code",
            ) from e

    return grant


def update_grant(grant: Fund, status: FundStatus | None = None):
    if status is not None:
        grant.proto_status = status

    db.session.add(grant)

    db.session.commit()
