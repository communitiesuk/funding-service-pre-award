import json
import string

import pytest
from bs4 import BeautifulSoup

from pre_award.apply.default.data import RoundStatus
from pre_award.apply.models.application_display_mapping import ApplicationMapping
from pre_award.apply.models.fund import Fund
from tests.pre_award.apply_tests.api_data.test_data import (
    SUBMITTED_APPLICATION,
    TEST_APPLICATION_SUMMARIES,
    TEST_APPLICATIONS,
    TEST_DISPLAY_DATA,
    TEST_FUNDS_DATA,
)
from tests.pre_award.apply_tests.utils import get_language_cookie_value

file = open("tests/pre_award/apply_tests/api_data/endpoint_data.json")
data = json.loads(file.read())
TEST_APPLICATION_EN = TEST_APPLICATIONS[0]
TEST_APPLICATION_CY = TEST_APPLICATIONS[1]

TEST_APPLICATION_DISPLAY_RESPONSE = data["fund_store/funds/funding-service-design/rounds/summer/sections/application"]


@pytest.fixture
def mock_applications(mocker):
    mocker.patch(
        "pre_award.apply.default.application_routes.get_application_data",
        return_value=TEST_APPLICATION_EN,
    )
    mocker.patch(
        "pre_award.apply.default.application_routes.determine_round_status",
        return_value=RoundStatus(False, False, True),
    )
    mocker.patch(
        "pre_award.apply.default.application_routes.get_application_display_config",
        return_value=[ApplicationMapping.from_dict(section) for section in TEST_APPLICATION_DISPLAY_RESPONSE],
    )


def test_tasklist_route(apply_test_client, mocker, mock_login, mock_applications, mock_tasklist_function_calls):
    mocker.patch(
        "pre_award.apply.default.application_routes.get_application_data",
        return_value=TEST_APPLICATION_EN,
    )
    response = apply_test_client.get("tasklist/test-application-id", follow_redirects=True)
    assert response.status_code == 200
    assert b"Help with filling out your application" in response.data
    assert b"Test Section 1" in response.data
    assert b"Risk" in response.data


def test_tasklist_route_after_deadline(apply_test_client, mocker, mock_login, mock_applications):
    mocker.patch(
        "pre_award.apply.default.application_routes.determine_round_status",
        return_value=RoundStatus(True, False, False),
    )
    response = apply_test_client.get("tasklist/test-application-id", follow_redirects=False)
    assert response.status_code == 302
    assert "/account" == response.location


def test_tasklist_for_submit_application_route(apply_test_client, mocker, mock_login):
    mocker.patch(
        "pre_award.apply.default.application_routes.get_application_data",
        return_value=SUBMITTED_APPLICATION,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.check_change_requested_for_applications",
        return_value=True,
    )
    mocker.patch(
        "pre_award.apply.default.application_routes.determine_round_status",
        return_value=RoundStatus(False, False, True),
    )

    get_apps_mock = mocker.patch(
        "pre_award.apply.default.account_routes.search_applications",
        return_value=TEST_APPLICATION_SUMMARIES,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.build_application_data_for_display",
        return_value=TEST_DISPLAY_DATA,
    )
    response = apply_test_client.get("tasklist/test-application-submit", follow_redirects=True)
    assert response.status_code == 200
    get_apps_mock.assert_called_once_with(
        search_params={
            "account_id": "test-user",
            "fund_id": "111",
            "round_id": "fsd-r2w2",
        },
        as_dict=False,
    )


def test_language_cookie_update_welsh_to_english(
    apply_test_client, mocker, mock_login, mock_applications, mock_tasklist_function_calls
):
    # set language cookie to welsh
    apply_test_client.set_cookie(domain="/", key="language", value="cy")

    # request an english application
    response = apply_test_client.get("tasklist/test-application-id", follow_redirects=True)

    # check cookie has been set to english
    assert response.status_code == 200
    current_set_language = get_language_cookie_value(response)

    assert current_set_language == "en"

    soup = BeautifulSoup(response.data, "html.parser")
    assert strip_all_ws(soup.find("a", class_="govuk-service-navigation__link").text) == strip_all_ws(
        "Apply for fund for testing"
    )


def test_language_cookie_update_english_to_welsh(
    apply_test_client, mocker, mock_login, mock_applications, mock_tasklist_function_calls
):
    # set language cookie to english
    apply_test_client.set_cookie(domain="/", key="language", value="en")

    # return welsh fund
    mocker.patch(
        "pre_award.apply.default.application_routes.get_fund_data",
        return_value=Fund.from_dict(TEST_FUNDS_DATA[2]),
    )
    # return welsh application
    mocker.patch(
        "pre_award.apply.default.application_routes.get_application_data",
        return_value=TEST_APPLICATION_CY,
    )

    # request a welsh application
    response = apply_test_client.get("tasklist/test-welsh-id", follow_redirects=True)

    # check cookie has been set to welsh
    assert response.status_code == 200
    current_set_language = get_language_cookie_value(response)

    assert current_set_language == "cy"

    soup = BeautifulSoup(response.data, "html.parser")
    assert strip_all_ws(soup.find("a", class_="govuk-service-navigation__link").text) == strip_all_ws(
        "Gwneud cais am gronfa cymraeg"
    )


def strip_all_ws(text):
    return text.translate({ord(c): None for c in string.whitespace})
