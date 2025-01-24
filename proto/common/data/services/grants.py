from datetime import date

import psycopg2
import sqlalchemy.exc
from flask_babel import lazy_gettext as _l
from sqlalchemy import select
from sqlalchemy.orm import joinedload

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
    round = (
        db.session.scalars(
            select(Round)
            .join(Fund)
            .filter(
                Fund.short_name == grant_short_code,
                # probably want some way of having rounds that are always open especially for uncompeted grants
                Round.proto_start_date <= date.today(),
                Round.proto_end_date >= date.today(),
            )
        )
        .unique()
        .one_or_none()
    )
    return round, round.proto_grant if round else None


def get_all_grants_with_rounds():
    return db.session.scalars(select(Fund).options(joinedload(Fund.rounds))).unique().all()


def create_grant(
    code,
    name,
    name_cy,
    title,
    title_cy,
    description,
    description_cy,
    welsh_available,
    funding_type,
    ggis_reference,
    prospectus_link,
):
    grant = Fund(
        name_json={"en": name, "cy": name_cy},  # Workaround: required field
        title_json={"en": title, "cy": title_cy},  # Workaround: required field
        short_name=code,
        description_json={"en": description, "cy": description_cy},  # Workaround: required field
        owner_organisation_name="todo",  # Workaround: required field
        owner_organisation_shortname="todo",  # Workaround: required field
        owner_organisation_logo_uri="todo",  # Workaround: required field
        funding_type=funding_type,
        welsh_available=welsh_available,
        ggis_scheme_reference_number=ggis_reference,
        proto_name=name,
        proto_name_cy=name_cy,
        proto_prospectus_link=prospectus_link,
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
