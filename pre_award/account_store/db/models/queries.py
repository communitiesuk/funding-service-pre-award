from sqlalchemy import select

from pre_award.account_store.db.models.account import Account
from pre_award.db import db
from pre_award.fund_store.db.models.round import Round


def get_email_address(account_id: str) -> str:
    query = select(Account.email).filter(Account.id == account_id)
    email = db.session.execute(query).scalar_one_or_none()
    if email is None:
        raise ValueError(f"No email address found for account ID {account_id}")
    return email


def set_application_reminder_sent(round: Round):
    round.application_reminder_sent = True
    db.session.commit()
