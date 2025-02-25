import random
import string
import uuid

from sqlalchemy import select

from db import db
from proto.common.data.models import (
    Fund,
    ProtoDataCollectionInstance,
    ProtoGrantRecipient,
    ProtoReport,
    ProtoReportingRound,
)


def _generate_report_code():
    return "".join(random.choices(string.ascii_uppercase, k=6))


def get_or_create_monitoring_reports_for_grant_recipient(grant_recipient: ProtoGrantRecipient) -> list[ProtoReport]:
    def _get_reports() -> list[ProtoReport]:
        return (
            db.session.scalars(
                select(ProtoReport)
                .join(ProtoReport.reporting_round)
                .join(ProtoReportingRound.grant)
                .join(Fund.recipients)
                .where(ProtoGrantRecipient.id == grant_recipient.id)
            )
            .unique()
            .all()
        )

    reports = _get_reports()

    if len(reports) != len(grant_recipient.grant.reporting_rounds):
        for reporting_round in grant_recipient.grant.reporting_rounds:
            if not any(report.reporting_round == reporting_round for report in reports):
                create_report(grant_recipient, reporting_round)

        reports = _get_reports()

    return reports


def get_report(id_: uuid.UUID) -> ProtoReport:
    return db.session.scalars(select(ProtoReport).where(ProtoReport.id == id_)).one()


def create_report(grant_recipient: ProtoGrantRecipient, reporting_round: ProtoReportingRound) -> ProtoReport:
    data_collection_instance = ProtoDataCollectionInstance()
    db.session.add(data_collection_instance)
    db.session.flush()

    report = ProtoReport(
        code=_generate_report_code(),
        fake=reporting_round.preview,
        reporting_round_id=reporting_round.id,
        organisation_id=grant_recipient.organisation_id,
        data_collection_instance_id=data_collection_instance.id,
    )
    db.session.add(report)
    db.session.commit()

    return report
