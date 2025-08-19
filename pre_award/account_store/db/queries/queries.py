from pre_award.account_store.db.models import Account, Role
from pre_award.db import db


def upsert_account(email: str, full_name: str):
    existing_account = Account.query.filter_by(
        email=email,
    ).first()

    if existing_account:
        existing_account.email = email
        existing_account.full_name = full_name
        db.session.flush()
        return existing_account
    else:
        new_account_row = Account(
            email=email,
            full_name=full_name,
        )
        db.session.add(new_account_row)
        db.session.flush()
        return new_account_row


def upsert_account_role(account: Account, role: str):
    existing_role = Role.query.filter_by(
        account_id=account.id,
        role=role,
    ).first()

    if existing_role:
        return existing_role
    else:
        new_role = Role(
            account_id=account.id,
            role=role,
        )
        db.session.add(new_role)
        db.session.flush()
        return new_role
