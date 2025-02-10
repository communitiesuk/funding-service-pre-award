from sqlalchemy import select

from pre_award.account_store.db.models import Account
from pre_award.db import db


def get_account(id_: str) -> Account | None:
    return db.session.scalar(select(Account).where(Account.id == id_))
