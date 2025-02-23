from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from db import db
from proto.common.data.models import Fund, ProtoReport, ProtoReportingRound
from proto.common.data.models.fund import FundStatus


def create_reporting_round(
    grant_id, reporting_period_starts, reporting_period_ends, submission_period_starts, submission_period_ends
):
    round = ProtoReportingRound(
        grant_id=grant_id,
        reporting_period_starts=reporting_period_starts,
        reporting_period_ends=reporting_period_ends,
        submission_period_starts=submission_period_starts,
        submission_period_ends=submission_period_ends,
    )
    db.session.add(round)

    db.session.commit()

    return round


def update_reporting_round(round: ProtoReport, preview: bool | None = None):
    if preview is not None:
        round.preview = preview

    db.session.add(round)

    db.session.commit()


def get_open_reporting_rounds() -> list[ProtoReportingRound]:
    return (
        db.session.scalars(
            select(ProtoReportingRound)
            .options(joinedload(ProtoReportingRound.grant))
            .filter(
                Fund.proto_status == FundStatus.LIVE,
                ProtoReportingRound.preview.is_(False),
                # probably want some way of having rounds that are always open especially for uncompeted grants
                ProtoReportingRound.submission_period_starts <= date.today(),
                ProtoReportingRound.submission_period_ends >= date.today(),
            )
        )
        .unique()
        .all()
    )


def get_reporting_round(reporting_round_id) -> ProtoReportingRound:
    return db.session.scalar(select(ProtoReportingRound).where(ProtoReportingRound.id == reporting_round_id))
