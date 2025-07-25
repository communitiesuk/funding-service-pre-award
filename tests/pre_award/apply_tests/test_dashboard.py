import json
from copy import deepcopy
from datetime import datetime
from unittest import mock
from unittest.mock import ANY

import pytest
from bs4 import BeautifulSoup

from pre_award.apply.default.account_routes import (
    build_application_data_for_display,
    determine_show_language_column,
    get_visible_funds,
    update_applications_statuses_for_display,
)
from pre_award.apply.default.data import RoundStatus
from pre_award.apply.models.application_summary import ApplicationSummary
from pre_award.apply.models.fund import Fund
from pre_award.config import Config
from tests.pre_award.apply_tests.api_data.test_data import (
    TEST_APPLICATION_SUMMARIES,
    TEST_DISPLAY_DATA,
    TEST_FUNDS_DATA,
    TEST_ROUNDS_DATA,
    common_application_data,
)
from tests.pre_award.apply_tests.utils import get_language_cookie_value

file = open("tests/pre_award/apply_tests/api_data/endpoint_data.json")
data = json.loads(file.read())
TEST_APPLICATION_STORE_JSON = data[
    "application_store/applications?account_id=" + "test-user&order_by=last_edited&order_rev=1"
]

TEST_SUBMITTED_APPLICATION_STORE_DATA = data["http://application_store/applications?account_id=test-user-2"]


def test_serialise_application_summary(app):
    application_list = TEST_APPLICATION_STORE_JSON

    applications = [ApplicationSummary.from_dict(application) for application in application_list]
    assert len(applications) == 3
    assert isinstance(applications[0].started_at, datetime)
    assert str(applications[0].started_at.tzinfo) == "Europe/London"
    assert applications[1].last_edited is None
    assert applications[1].language == "English"
    assert applications[2].language == "Welsh"


@pytest.mark.parametrize(
    "fund_short_name,round_short_name,expected_search_params",
    [
        (
            "COF",
            "R2W2",
            {
                "account_id": "test-user",
                "round_id": "fsd-r2w2",
                "fund_id": "111",
            },
        ),
        (
            "COF",
            None,
            {
                "account_id": "test-user",
                "fund_id": "111",
            },
        ),
    ],
)
def test_dashboard_route_search_call(
    apply_test_client,
    mocker,
    app,
    mock_login,
    fund_short_name,
    round_short_name,
    expected_search_params,
):
    mocker.patch(
        "pre_award.apply.default.account_routes.check_change_requested_for_applications",
        return_value=True,
    )
    request_mock = mocker.patch("pre_award.apply.default.account_routes.request")
    request_mock.args.get = (
        lambda key, default: fund_short_name if key == "fund" else (round_short_name if key == "round" else default)
    )
    get_apps_mock = mocker.patch(
        "pre_award.apply.default.account_routes.search_applications",
        return_value=TEST_APPLICATION_SUMMARIES,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.build_application_data_for_display",
        return_value=TEST_DISPLAY_DATA,
    )
    response = apply_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200

    get_apps_mock.assert_called_once_with(search_params=expected_search_params, as_dict=False)


@pytest.mark.parametrize(
    "query_string,exp_template_name",
    [
        ("?fund=abc&round=123", "apply/dashboard_single_fund.html"),
        ("?fund=abc", "apply/dashboard_single_fund.html"),
    ],
)
def test_dashboard_template_rendered(
    apply_test_client,
    mock_login,
    mocker,
    templates_rendered,
    query_string,
    exp_template_name,
):
    mocker.patch(
        "pre_award.apply.default.account_routes.check_change_requested_for_applications",
        return_value=True,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.search_applications",
        return_value=TEST_APPLICATION_SUMMARIES,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.build_application_data_for_display",
        return_value=TEST_DISPLAY_DATA,
    )

    response = apply_test_client.get(f"/account{query_string}", follow_redirects=True)
    assert response.status_code == 200
    assert 1 == len(templates_rendered)
    rendered_template = templates_rendered[0]
    assert exp_template_name == rendered_template[0].name


def test_dashboard_eoi_suffix(
    apply_test_client,
    mock_login,
    mocker,
):
    eoi_data = deepcopy(TEST_DISPLAY_DATA)
    eoi_data["funds"][0]["fund_data"]["funding_type"] = "EOI"
    mocker.patch(
        "pre_award.apply.default.account_routes.check_change_requested_for_applications",
        return_value=True,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.search_applications",
        return_value=TEST_APPLICATION_SUMMARIES,
    )
    mocker.patch("pre_award.apply.default.account_routes.build_application_data_for_display", return_value=eoi_data)

    response = apply_test_client.get("/account?fund=COF-EOI&round=R1", follow_redirects=True)

    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    assert "Expression of interest" in soup.find("span", class_="govuk-caption-m").get_text()


@pytest.mark.parametrize(
    "query_string,fund_supports_welsh,requested_language,exp_response_language",
    [
        ("?fund=abc&round=123", True, "en", "en"),
        ("?fund=abc&round=123", True, "cy", "cy"),
        ("?fund=abc&round=123", False, "cy", "en"),
        ("?fund=abc&round=123", False, "en", "en"),
    ],
)
def test_dashboard_language(
    apply_test_client,
    mock_login,
    mocker,
    query_string,
    fund_supports_welsh,
    requested_language,
    exp_response_language,
):
    mocker.patch(
        "pre_award.apply.default.account_routes.check_change_requested_for_applications",
        return_value=True,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.search_applications",
        return_value=TEST_APPLICATION_SUMMARIES,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.build_application_data_for_display",
        return_value=TEST_DISPLAY_DATA,
    )
    mocker.patch("pre_award.apply.default.account_routes.get_lang", return_value=requested_language)

    mocker.patch(
        "pre_award.apply.helpers.get_fund",
        return_value=Fund.from_dict(
            {
                "id": "111",
                "name": "Test Fund",
                "description": "test test",
                "short_name": "FSD",
                "title": "fund for testing",
                "funding_type": "COMPETITIVE",
                "welsh_available": fund_supports_welsh,
            },
        ),
    )
    response = apply_test_client.get(f"/account{query_string}", follow_redirects=True)
    assert response.status_code == 200
    assert exp_response_language == get_language_cookie_value(response=response)


def test_dashboard_route(apply_test_client, mocker, mock_login):
    mocker.patch(
        "pre_award.apply.default.account_routes.check_change_requested_for_applications",
        return_value=True,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.search_applications",
        return_value=TEST_APPLICATION_SUMMARIES,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.build_application_data_for_display",
        return_value=TEST_DISPLAY_DATA,
    )
    response = apply_test_client.get("/account?fund=COF&round=R2W3", follow_redirects=True)
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, "html.parser")

    assert len(soup.find_all("strong", class_="in-progress-tag-new")) == 1
    assert len(soup.find_all("strong", class_="govuk-tag--yellow")) == 1
    assert len(soup.find_all("strong", class_="complete-tag")) == 2

    continue_application_links = [link for link in soup.find_all("a") if "Continue application" in link.get_text()]
    assert len(continue_application_links) == 2

    assert (
        len(
            soup.find_all(
                "h2",
                string=lambda text: "Window closed - Test Fund " + "Round 2 Window 2" in text,
            )
        )
        == 1
    )
    assert (
        len(
            soup.find_all(
                "h2",
                string=lambda text: "Window closed - Community Ownership Fund " + "Round 2 Window 2" in text,
            )
        )
        == 0
    )
    assert len(soup.find_all("span", class_="govuk-caption-m", string=lambda text: "Test Fund" == str.strip(text))) == 2
    assert len(soup.find_all("h2", string=lambda text: "Round 2 Window 2" == str.strip(text))) == 1
    assert len(soup.find_all("h2", string=lambda text: "Round 2 Window 2" == str.strip(text))) == 1


def test_account_dashboard_with_no_fund_or_round_doesnt_500(apply_test_client, mocker, mock_login, mock_get_fund_round):
    response = apply_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 404


@pytest.mark.parametrize(
    "funds,rounds,applications,expected_fund_count,expected_round_count,expected_app_count,"
    " fund_short_name,round_short_name",
    [
        # No filters, 2 funds with 2 rounds each
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA,
            TEST_APPLICATION_SUMMARIES,
            2,
            4,
            4,
            None,
            None,
        ),
        # No fund filter, one fund with no rounds one fund with 2 rounds
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA[0:2],
            TEST_APPLICATION_SUMMARIES,
            1,
            2,
            2,
            None,
            None,
        ),
        # Filter to fund with open rounds
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA,
            TEST_APPLICATION_SUMMARIES,
            1,
            2,
            2,
            "FSD",
            None,
        ),
        # Filter to fund with no rounds
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA[0:2],
            TEST_APPLICATION_SUMMARIES,
            0,
            0,
            0,
            "FSD2",
            None,
        ),
        # 1 app in closed round, 0 in open round
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA,
            TEST_APPLICATION_SUMMARIES[0:1],
            1,
            2,
            1,
            "FSD",
            None,
        ),
        # 1 app in closed round, 0 in open round - filter to closed round
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA,
            TEST_APPLICATION_SUMMARIES[0:1],
            1,
            1,
            1,
            "FSD",
            "r2w2",
        ),
        # 1 app in closed round, 0 in open round - filter to open round
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA,
            TEST_APPLICATION_SUMMARIES[0:1],
            1,
            1,
            0,
            "FSD",
            "r2w3",
        ),
        # 1 app in open round, 0 in closed round
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA,
            TEST_APPLICATION_SUMMARIES[1:2],
            1,
            1,
            1,
            "FSD",
            None,
        ),
        # 1 fund with 2 rounds and 2 apps, 1 fund with 1 closed round and no
        # apps
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA[0:3],
            TEST_APPLICATION_SUMMARIES[0:2],
            1,
            2,
            2,
            None,
            None,
        ),
        # 1 open round, 0 applications
        (
            TEST_FUNDS_DATA[0:1],
            TEST_ROUNDS_DATA[1:2],
            [],
            1,
            1,
            0,
            None,
            None,
        ),
    ],
)
def test_build_application_data_for_display(
    funds,
    rounds,
    applications,
    expected_fund_count,
    expected_round_count,
    expected_app_count,
    fund_short_name,
    round_short_name,
    mocker,
):
    mocker.patch(
        "pre_award.apply.default.account_routes.get_all_funds",
        return_value=funds,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.get_all_rounds_for_fund",
        new=lambda fund_id, language, as_dict, ttl_hash: [round for round in rounds if round.fund_id == fund_id],
    )

    result = build_application_data_for_display(applications, fund_short_name, round_short_name)

    assert result["total_applications_to_display"] == expected_app_count
    assert len(result["funds"]) == expected_fund_count
    assert sum(len(fund["rounds"]) for fund in result["funds"]) == expected_round_count


@pytest.mark.parametrize(
    "application,round_status,expected_status",
    [
        (
            ApplicationSummary.from_dict({**common_application_data, "status": "IN_PROGRESS"}),
            RoundStatus(False, False, True),
            "IN_PROGRESS",
        ),
        (
            ApplicationSummary.from_dict({**common_application_data, "status": "COMPLETED"}),
            RoundStatus(False, False, True),
            "READY_TO_SUBMIT",
        ),
        (
            ApplicationSummary.from_dict({**common_application_data, "status": "COMPLETED"}),
            RoundStatus(True, False, False),
            "NOT_SUBMITTED",
        ),
        (
            ApplicationSummary.from_dict({**common_application_data, "status": "IN_PROGRESS"}),
            RoundStatus(True, False, False),
            "NOT_SUBMITTED",
        ),
    ],
)
def test_update_application_statuses(application, round_status, expected_status):
    result = update_applications_statuses_for_display([application], round_status)
    assert result[0].status == expected_status


@pytest.mark.parametrize(
    "applications,exp_visible",
    [
        (
            [
                ApplicationSummary.from_dict({**common_application_data, "language": "en"}),
                ApplicationSummary.from_dict({**common_application_data, "language": "cy"}),
            ],
            True,
        ),
        (
            [
                ApplicationSummary.from_dict({**common_application_data, "language": "cy"}),
                ApplicationSummary.from_dict({**common_application_data, "language": "cy"}),
            ],
            False,
        ),
        (
            [
                ApplicationSummary.from_dict({**common_application_data, "language": "en"}),
                ApplicationSummary.from_dict({**common_application_data, "language": "en"}),
            ],
            False,
        ),
        ([], False),
    ],
)
def test_determine_show_language_column(applications, exp_visible):
    assert exp_visible == determine_show_language_column(applications=applications)


@pytest.mark.parametrize(
    "funds, filter_value, expected_count",
    [
        ([{"short_name": "ABC"}], "ABC", 1),
        ([{"short_name": "ABC"}], "abc", 1),
        ([{"short_name": "ABC"}], "def", 0),
        ([], "ABC", 0),
        ([{"short_name": "ABC"}, {"short_name": "DEF"}], "abc", 1),
    ],
)
def test_filter_funds_by_short_name(funds, filter_value, expected_count, mocker):
    mocker.patch("pre_award.apply.default.account_routes.get_all_funds", return_value=funds)
    result = get_visible_funds(filter_value)
    assert expected_count == len(result)


@pytest.mark.parametrize(
    "cookie_lang,fund_supports_welsh,exp_application_lang",
    [
        ("en", True, "en"),
        ("en", False, "en"),
        ("cy", True, "cy"),
        ("cy", False, "en"),
    ],
)
def test_create_new_application(
    apply_test_client,
    mocker,
    app,
    mock_login,
    cookie_lang,
    fund_supports_welsh,
    exp_application_lang,
):
    mock_app_store_response = mock.MagicMock()
    mock_app_store_response.status_code = 201
    post_request = mocker.patch(
        "pre_award.apply.default.account_routes.requests.post",
        return_value=mock_app_store_response,
    )
    mocker.patch("pre_award.apply.default.account_routes.get_lang", return_value=cookie_lang)
    mock_fund = mock.MagicMock()
    mock_fund.welsh_available = fund_supports_welsh
    mocker.patch("pre_award.apply.default.account_routes.get_fund", return_value=mock_fund)

    request_mock = mocker.patch("pre_award.apply.default.account_routes.request")
    request_mock.form = {"fund_id": "test-fund-id", "round_id": "test-round-id"}
    request_mock.method = "POST"
    response = apply_test_client.post("/account/new", data=request_mock.form, follow_redirects=False)

    assert 302 == response.status_code
    # assert the request to app store to create the application uses the expected language
    post_request.assert_called_once_with(
        url=f"{Config.APPLICATION_STORE_API_HOST}/applications",
        json={
            "account_id": "test-user",
            "round_id": ANY,
            "fund_id": ANY,
            "language": exp_application_lang,
        },
    )
