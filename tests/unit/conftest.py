import copy
from datetime import datetime
from typing import Any

import pytest
from flask import template_rendered
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from data.models import Fund, Round
from pre_award.config.envs.unit_test import UnitTestConfig
from pre_award.fund_store.config.fund_loader_config.FAB.ctdf import LOADER_CONFIG as ctdf_config


def _convert_fab_config_into_format_from_db(config_values: dict) -> dict:
    result = copy.deepcopy(config_values)
    for key in ["opens", "assessment_start", "deadline", "reminder_date", "assessment_deadline"]:
        result.update(
            {
                key: datetime.strptime(config_values[key], "%Y-%m-%dT%H:%M:%S"),
            }
        )
    return result


mock_fund = Fund(**ctdf_config["fund_config"])
mock_round_open = Round(fund=mock_fund, **_convert_fab_config_into_format_from_db(ctdf_config["round_config"]))

mock_round_closed = Round(
    fund=mock_fund,
    title_json={"en": "Crash Round Closed", "cy": None},
    deadline=datetime(2024, 12, 31, 11, 58, 0),  # Deadline in the past to trigger "Window closed"
    instructions_json={
        "en": "This is a fake fund for testing so will not result in you getting any money!",
        "cy": None,
    },
)


# this is temp copied from apply_tests while the new routes are piggy backing on the apply
# host (frontend.access-funding....)
# TODO remove this once we have a single host name
class _ApplyFlaskClient(FlaskClient):
    def open(
        self,
        *args: Any,
        buffered: bool = False,
        follow_redirects: bool = False,
        **kwargs: Any,
    ) -> TestResponse:
        if "headers" in kwargs:
            kwargs["headers"].setdefault("Host", UnitTestConfig.APPLY_HOST)
        else:
            kwargs.setdefault("headers", {"Host": UnitTestConfig.APPLY_HOST})
        return super().open(*args, buffered=buffered, follow_redirects=follow_redirects, **kwargs)


@pytest.fixture()
def apply_test_client(app):
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """
    app.test_client_class = _ApplyFlaskClient
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(scope="function")
def templates_rendered(app):
    """
    A pytest fixture that records all rendered templates for this test function.

    To access the templates that were rendered:
    ```
    rendered_template = templates_rendered[0]
    assert "expected/template/path.html.jinja" == rendered_template[0].name
    assert "Test fund name" == rendered_template[1]["fund"].fund_name
    ```
    """
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture()
def mock_get_round_success(mocker):
    mocker.patch("apply.routes.get_round", return_value=mock_round_open)
    mocker.patch("app.find_fund_and_round_in_request", return_value=(mock_fund, mock_round_open))
    mocker.patch("app.find_fund_in_request", return_value=mock_fund)


@pytest.fixture()
def mock_get_fund_success(mocker):
    mocker.patch("apply.routes.get_fund", return_value=mock_fund)
