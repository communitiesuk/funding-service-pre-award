import uuid

from sqlalchemy import case, select

from db import db
from proto.common.data.models import Fund, ProtoApplication, ProtoGrantRecipient, Round
from proto.common.data.models.fund import FundingType
from proto.common.data.models.recipients import GrantRecipientStatus


def search_recipients(short_code):
    recipients = db.session.scalars(
        select(ProtoGrantRecipient)
        .join(ProtoGrantRecipient.application)
        .join(ProtoApplication.round)
        .join(Round.proto_grant)
        .filter(
            Fund.short_name == short_code,
            case((Fund.funding_type == FundingType.COMPETITIVE, ProtoApplication.submitted), else_=True),
        )
    ).all()
    return recipients


def get_grant_recipients_for_account(account_id):
    recipients = db.session.scalars(
        select(ProtoGrantRecipient)
        .join(ProtoGrantRecipient.application)
        .filter(
            ProtoApplication.account_id == account_id,
        )
    ).all()
    return recipients


def get_grant_recipient_for_account(account_id, short_code: str):
    recipient = db.session.scalar(
        select(ProtoGrantRecipient)
        .join(ProtoGrantRecipient.application)
        .join(ProtoApplication.round)
        .join(Round.proto_grant)
        .filter(
            ProtoApplication.account_id == account_id,
            Fund.short_name == short_code,
        )
    )
    return recipient


def create_recipient_from_application(application: ProtoApplication):
    recipient = ProtoGrantRecipient(
        status=GrantRecipientStatus.ACTIVE, application=application, grant_id=application.round.fund_id
    )
    db.session.add(recipient)

    db.session.commit()
    return recipient


def get_grant_recipient(short_code: str, recipient_id: uuid.UUID):
    return db.session.scalar(
        select(ProtoGrantRecipient)
        .join(ProtoGrantRecipient.application)
        .join(ProtoApplication.round)
        .join(Round.proto_grant)
        .filter(ProtoGrantRecipient.id == recipient_id, Fund.short_name == short_code)
    )


def update_grant_recipient(
    recipient: ProtoGrantRecipient, funding_allocated: int | None = None, funding_paid: int | None = None
):
    if funding_allocated is not None:
        recipient.funding_allocated = funding_allocated

    if funding_paid is not None:
        recipient.funding_paid = funding_paid

    db.session.commit()
