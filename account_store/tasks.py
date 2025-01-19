import os
from contextlib import contextmanager
from uuid import uuid4

from colored import attr, fg, stylize
from invoke import task
from sqlalchemy import select

from account_store.db.models.account import Account
from account_store.db.models.role import Role  # noqa:E402
from app import create_app

ECHO_STYLE = fg("blue") + attr("bold")
DB_NAME = "fsd_account_store_dev"


@contextmanager
def _env_var(key, value):
    old_val = os.environ.get(key, "")
    os.environ[key] = value
    yield
    os.environ[key] = old_val


@task
def bootstrap_dev_db(c, database_host="localhost"):
    """Create a clean database for testing"""
    c.run(f"dropdb -h {database_host} --if-exists {DB_NAME}")
    print(stylize(f"{DB_NAME} db dropped...", ECHO_STYLE))
    c.run(f"createdb -h {database_host} {DB_NAME}")
    print(stylize(f"{DB_NAME} db created...", ECHO_STYLE))


def seed_local_account_store_impl():
    from db import db

    accounts_to_seed = [
        {
            "email": "lead_assessor@example.com",
            "account_id": uuid4(),
            "roles": [
                "CTDF_LEAD_ASSESSOR",
                "CTDF_ASSESSOR",
                "CTDF_COMMENTER",
                "FFW_LEAD_ASSESSOR",
                "FFW_ASSESSOR",
                "FFW_COMMENTER",
            ],
        },
        {
            "email": "dev@example.com",
            "account_id": "00000000-0000-0000-0000-000000000000",
            "roles": [],
        },
    ]  # seed this in the db so it exists in account_store
    for account_to_create in accounts_to_seed:
        account_from_db = db.session.query(Account).where(Account.email == account_to_create["email"]).one_or_none()
        if not account_from_db:
            # Create account
            account = Account(id=account_to_create["account_id"], email=account_to_create["email"])
            db.session.add(account)
            db.session.commit()
            print(f"Created account for {account_to_create['email']}")

        else:
            print(f"Account {account_to_create['email']} already exists")
            account_to_create["account_id"] = account_from_db.id

        existing_roles = db.session.scalars(
            select(Role.role).where(Role.account_id == account_to_create["account_id"])
        ).all()

        roles_to_add = []

        for required_role in account_to_create["roles"]:
            if required_role not in existing_roles:
                req_role = Role(id=uuid4(), account_id=account_to_create["account_id"], role=required_role)
                roles_to_add.append(req_role)
                print(f"Creating role {required_role} for {account_to_create['email']}")

        db.session.bulk_save_objects(roles_to_add)
        db.session.commit()


@task
def seed_local_account_store(c):
    with _env_var("FLASK_ENV", "development"):
        app = create_app()
        with app.app_context():
            seed_local_account_store_impl()
