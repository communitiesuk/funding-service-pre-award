import types
from contextlib import contextmanager
from typing import Any, Generator
from unittest import mock

import jwt as jwt
import pytest
from flask import current_app
from flask.sessions import SessionMixin
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from pre_award.apply.models.application_summary import ApplicationSummary
from pre_award.authenticator.models.account import AccountMethods
from pre_award.config.envs.unit_test import UnitTestConfig
from tests.pre_award.authenticator_tests.testing.mocks.mocks import *  # noqa


@pytest.fixture
def app_context(app):
    with app.app_context():
        with current_app.test_request_context():
            yield


@pytest.fixture(scope="function")
def create_magic_link(mocker, mock_notification_service_calls):
    from pre_award.authenticator.models.fund import Fund
    from pre_award.authenticator.models.round import Round

    mocker.patch(
        "pre_award.authenticator.models.account.FundMethods.get_fund",
        return_value=Fund(
            name="test fund", fund_title="hello", short_name="COF", identifier="asdfasdf", description="asdfasdfasdf"
        ),
    )
    mocker.patch(
        "pre_award.authenticator.models.account.get_round_data", return_value=Round(contact_email="asdf@asdf.com")
    )
    mocker.patch(
        "pre_award.authenticator.api.magic_links.routes.get_round_data",
        return_value=Round(contact_email="asdf@asdf.com"),
    )
    auth_landing = AccountMethods.get_magic_link("a@example.com", "cof", "r1w1")
    link_key_end = auth_landing.index("?fund=")
    link_key = auth_landing[link_key_end - 8 : link_key_end]  # noqa:E203
    yield link_key


def patch_get_applications_for_account(path):
    return mock.patch(
        path,
        return_value=[
            ApplicationSummary(
                id="00000000-0000-0000-0000-000000000000",
                reference="TEST-REFERENCE",
                status="NOT_STARTED",
                round_id="00000000-0000-0000-0000-000000000000",
                fund_id="00000000-0000-0000-0000-000000000000",
                started_at="2025-01-07T15:22:08.422538+00:00",
                project_name=None,
                language="English",
                last_edited="2025-01-07T15:22:08.422538+00:00",
            )
        ],
    )


@pytest.fixture
def mock_get_applications_for_auth_api():
    with patch_get_applications_for_account(
        "authenticator.api.magic_links.routes.get_applications_for_account"
    ) as mock_get_applications:
        yield mock_get_applications


@pytest.fixture
def mock_get_applications_for_auth_frontend():
    with patch_get_applications_for_account(
        "pre_award.authenticator.frontend.magic_links.routes.get_applications_for_account"
    ) as mock_get_applications:
        yield mock_get_applications


def configure_mock_fund_and_round(mock_get_fund, mock_get_round_data):
    mock_fund = mock.MagicMock()
    mock_fund.configure_mock(name="cof")
    mock_fund.configure_mock(short_name="cof")
    mock_get_fund.return_value = mock_fund

    mock_round = mock.MagicMock()
    mock_round.configure_mock(deadline="2023-01-30T00:00:01")
    mock_round.configure_mock(title="r2w3")
    mock_round.configure_mock(short_name="r2w3")
    mock_round.configure_mock(application_guidance="help text here")
    mock_round.configure_mock(contact_email="test@outlook.com")
    mock_round.configure_mock(reference_contact_page_over_email=False)
    mock_round.configure_mock(is_expression_of_interest=False)
    mock_round.configure_mock(has_eligibility=True)
    mock_get_round_data.return_value = mock_round


@pytest.fixture(autouse=True)
def patch_app_find_round(mocker):
    stub_round = types.SimpleNamespace(
        id="Test_fund_round_id",
        short_name="r2w2",
        fund_short_name="cof",
        privacy_notice="https://privacy.com",
        title="r2w2",
        deadline="2050-01-01T00:00:01",
    )
    mocker.patch("app.find_round_in_request", return_value=stub_round)

    yield


@pytest.fixture
def mock_get_applications_for_account():
    from unittest import mock

    with mock.patch(
        "pre_award.authenticator.api.magic_links.routes.get_applications_for_account"
    ) as mock_get_applications:
        mock_get_applications.return_value = [
            ApplicationSummary(
                id="00000000-0000-0000-0000-000000000000",
                reference="TEST-REFERENCE",
                status="NOT_STARTED",
                round_id="00000000-0000-0000-0000-000000000000",
                fund_id="00000000-0000-0000-0000-000000000000",
                started_at="2025-01-07T15:22:08.422538+00:00",
                project_name=None,
                language="English",
                last_edited="2025-01-07T15:22:08.422538+00:00",
            )
        ]
        yield mock_get_applications


class _AuthenticatorFlaskClient(FlaskClient):
    def open(
        self,
        *args: Any,
        buffered: bool = False,
        follow_redirects: bool = False,
        **kwargs: Any,
    ) -> TestResponse:
        if "headers" in kwargs:
            kwargs["headers"].setdefault("Host", UnitTestConfig.AUTH_HOST)
        else:
            kwargs.setdefault("headers", {"Host": UnitTestConfig.AUTH_HOST})
        return super().open(*args, buffered=buffered, follow_redirects=follow_redirects, **kwargs)

    def set_cookie(
        self,
        key: str,
        value: str = "",
        *,
        domain: str | None = None,
        origin_only: bool = False,
        path: str = "/",
        **kwargs: Any,
    ) -> None:
        if domain is None:
            domain = self.application.config["COOKIE_DOMAIN"]
        super().set_cookie(key=key, value=value, domain=domain, origin_only=origin_only, path=path, **kwargs)

    @contextmanager
    def session_transaction(self, *args: Any, **kwargs: Any) -> Generator[SessionMixin, None, None]:
        if "headers" in kwargs:
            kwargs["headers"].setdefault("Host", UnitTestConfig.AUTH_HOST)
        else:
            kwargs.setdefault("headers", {"Host": UnitTestConfig.AUTH_HOST})
        with super().session_transaction(*args, **kwargs) as sess:
            yield sess


@pytest.fixture()
def authenticator_test_client(app, user_token=None):
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """

    app.test_client_class = _AuthenticatorFlaskClient

    with app.app_context() as app_context:
        with app_context.app.test_client() as test_client:
            yield test_client
