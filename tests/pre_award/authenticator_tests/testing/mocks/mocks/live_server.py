import pytest
from flask import Flask

from app import create_app


@pytest.fixture(scope="session")
def app(request) -> Flask:
    app = create_app()
    request.getfixturevalue("mock_redis")
    yield app
