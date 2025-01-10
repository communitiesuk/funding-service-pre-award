"""
Contains test configuration.
"""

from typing import Any
from uuid import uuid4

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from app import create_app  # noqa: E402
from pre_award.account_store.db.models.account import Account
from pre_award.account_store.db.models.role import Role
from pre_award.config import Config


@pytest.fixture(scope="session")
def app(request) -> Flask:
    app = create_app()
    request.getfixturevalue("mock_redis")
    yield app


class _FlaskClientWithHost(FlaskClient):
    def open(
        self,
        *args: Any,
        buffered: bool = False,
        follow_redirects: bool = False,
        **kwargs: Any,
    ) -> TestResponse:
        if "headers" in kwargs:
            kwargs["headers"].setdefault("Host", Config.API_HOST)
        else:
            kwargs.setdefault("headers", {"Host": Config.API_HOST})
        return super().open(*args, buffered=buffered, follow_redirects=follow_redirects, **kwargs)


@pytest.fixture(scope="session")
def flask_test_client(app):
    app.test_client_class = _FlaskClientWithHost
    yield app.test_client()


test_user_1 = {
    "email": "seeded_user_1@example.com",
    "subject_id": "subject_id_1",
    "account_id": uuid4(),
    "roles": ["COMMENTER"],
}
test_user_2 = {
    "email": "seeded_user_2@example.com",
    "subject_id": "subject_id_2",
    "account_id": uuid4(),
    "roles": ["COMMENTER"],
}
test_user_to_update = {
    "email": "seeded_user_x@example.com",
    "subject_id": "subject_id_x",
    "account_id": uuid4(),
    "roles": ["COMMENTER"],
}


def create_user_with_roles(user_config, db):
    new_account = Account(
        email=user_config["email"],
        azure_ad_subject_id=user_config["subject_id"],
        id=user_config["account_id"],
    )
    db.session.add(new_account)
    db.session.commit()

    roles_to_add = []
    for r in user_config["roles"]:
        role = Role(account_id=user_config["account_id"], role=r)
        roles_to_add.append(role)
    db.session.add_all(roles_to_add)

    db.session.commit()


@pytest.fixture(scope="session")
def seed_test_data(request, app, clear_test_data, _db):
    marker = request.node.get_closest_marker("user_config")
    if not marker:
        users_to_create = [test_user_1, test_user_2, test_user_to_update]
    else:
        users_to_create = marker.args[0]
    for user in users_to_create:
        create_user_with_roles(user, _db)
    yield users_to_create


@pytest.fixture(scope="function")
def seed_test_data_fn(request, app, clear_test_data, _db):
    marker = request.node.get_closest_marker("user_config")
    if not marker:
        users_to_create = [test_user_1, test_user_2, test_user_to_update]
    else:
        users_to_create = marker.args[0]
    for user in users_to_create:
        create_user_with_roles(user, _db)
    yield users_to_create
    Role.query.delete()
    Account.query.delete()
    _db.session.commit()
