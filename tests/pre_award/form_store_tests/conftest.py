"""
Contains test configuration for form_store tests.
"""

from datetime import datetime
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from pre_award.config import Config
from pre_award.form_store.db.models.form_definition import FormDefinition


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


@pytest.fixture(scope="function", autouse=True)
def mock_auth():
    """Mock authentication for all tests."""
    mock_payload = {
        "accountId": "test-account-id",
        "fullName": "Test User",
        "email": "test@example.com",
        "roles": ["ADMIN"],
    }

    # Mock the entire _check_access_token function to always return valid payload
    with patch("fsd_utils.authentication.decorators._check_access_token") as mock_check:
        mock_check.return_value = mock_payload
        with patch("fsd_utils.authentication.decorators.User.set_with_token") as mock_user_set:
            mock_user = MagicMock()
            mock_user.email = "test@example.com"
            mock_user.full_name = "Test User"
            mock_user.roles = ["ADMIN"]
            mock_user.highest_role_map = {}
            mock_user_set.return_value = mock_user

            yield


@pytest.fixture(scope="function")
def flask_test_client(app, db):
    """Create test client with authentication mocked."""
    app.test_client_class = _FlaskClientWithHost
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(scope="function", autouse=True)
def cleanup_forms(db):
    """Clean up all forms after each test."""
    yield
    # This runs after each test
    try:
        FormDefinition.query.delete()
        db.session.commit()
    except Exception:
        db.session.rollback()


@pytest.fixture(scope="function")
def sample_form_data():
    """Sample form JSON data for testing."""
    return {
        "name": "test-form",
        "form_json": {
            "pages": [
                {
                    "path": "/test-page",
                    "title": "Test Page",
                    "components": [{"name": "test-field", "title": "Test Field", "type": "TextField"}],
                }
            ],
            "startPage": "/test-page",
        },
    }


@pytest.fixture(scope="function")
def sample_form_record(db, sample_form_data):
    """Create a sample form record in the database."""
    form = FormDefinition(name=sample_form_data["name"], draft_json=sample_form_data["form_json"], published_json={})
    db.session.add(form)
    db.session.commit()
    yield form


@pytest.fixture(scope="function")
def published_form_record(db):
    """Create a sample form record with published content."""
    form_json = {
        "pages": [{"path": "/published-page", "title": "Published Page", "components": []}],
        "startPage": "/published-page",
    }

    form = FormDefinition(
        name="published-form",
        draft_json=form_json,
        published_json=form_json,
        published_at=datetime.now(),
    )
    db.session.add(form)
    db.session.commit()
    yield form


@pytest.fixture(scope="function")
def multiple_form_records(db):
    """Create multiple form records for testing."""
    forms = []
    form_data = [
        {
            "name": "form-1",
            "draft_json": {"title": "Form 1", "pages": []},
            "published_json": {"title": "Form 1", "pages": []},
            "published_at": datetime.now(),
        },
        {"name": "form-2", "draft_json": {"title": "Form 2", "pages": []}, "published_json": {}},
        {"name": "form-3", "draft_json": {"title": "Form 3", "pages": []}, "published_json": {}},
    ]

    for data in form_data:
        form = FormDefinition(**data)
        db.session.add(form)
        forms.append(form)

    db.session.commit()
    yield forms
