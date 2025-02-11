"""
Contains test configuration.
"""

import multiprocessing
import platform
import uuid
from multiprocessing import Process

import pytest
from flask import Flask
from flask_migrate import upgrade
from sqlalchemy_utils import create_database, database_exists
from testcontainers.postgres import PostgresContainer

from services.notify import Notification
from tests.pre_award.authenticator_tests.testing.mocks.mocks.redis_magic_links import RedisMLinks
from tests.pre_award.authenticator_tests.testing.mocks.mocks.redis_sessions import RedisSessions

if platform.system() == "Darwin":
    multiprocessing.set_start_method("fork")  # Required on macOSX


@pytest.fixture(scope="session")
def setup_db_container():
    test_postgres = PostgresContainer("postgres:16")
    test_postgres.start()
    from pre_award.config.envs.unit_test import UnitTestConfig

    UnitTestConfig.SQLALCHEMY_DATABASE_URI = test_postgres.get_connection_url()
    yield
    test_postgres.stop()


@pytest.fixture(scope="session")
def app(setup_db_container, request) -> Flask:
    from app import create_app  # noqa: E402

    app = create_app()
    request.getfixturevalue("mock_redis")
    yield app


@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        no_db = not database_exists(app.config["SQLALCHEMY_DATABASE_URI"])

        if no_db:
            create_database(app.config["SQLALCHEMY_DATABASE_URI"])

        # Run alembic migrations. We do this is a separate python process because it loads and executes a bunch
        # of code from db/migrations/env.py. This does things like set up loggers, which interferes with the
        # `caplog` fixture, and possibly has some other unexpected side effects.
        proc = Process(target=upgrade)
        proc.start()
        proc.join()

        yield app.extensions["sqlalchemy"]


@pytest.fixture(scope="session")
def mock_redis(session_mocker):
    session_mocker.patch("redis.Redis.get", RedisSessions.get)
    session_mocker.patch("redis.Redis.set", RedisSessions.set)
    session_mocker.patch("redis.Redis.delete", RedisSessions.delete)
    session_mocker.patch("redis.Redis.setex", RedisSessions.setex)
    session_mocker.patch("app.redis_mlinks.client_list", RedisMLinks.client_list)
    yield


@pytest.fixture(scope="function")
def flask_test_client(app):
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(scope="function")
def mock_notification_service_calls(mocker):
    calls = []

    mocker.patch(
        "services.notify.NotificationService._send_email",
        side_effect=lambda *args, **kwargs: calls.append(mocker.call(*args, **kwargs)) or Notification(id=uuid.uuid4()),
    )

    yield calls
