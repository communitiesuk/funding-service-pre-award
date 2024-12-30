"""
Contains test configuration.
"""

import multiprocessing
import platform

import pytest
from flask import Flask

from app import create_app  # noqa: E402
from tests.authenticator_tests.testing.mocks.mocks.redis_magic_links import RedisMLinks
from tests.authenticator_tests.testing.mocks.mocks.redis_sessions import RedisSessions

if platform.system() == "Darwin":
    multiprocessing.set_start_method("fork")  # Required on macOSX

pytest_plugins = ["fsd_test_utils.fixtures.db_fixtures"]


@pytest.fixture(scope="session")
def app(request) -> Flask:
    app = create_app()
    request.getfixturevalue("mock_redis")
    yield app


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
        side_effect=lambda *args, **kwargs: calls.append(mocker.call(*args, **kwargs)),
    )

    yield calls
