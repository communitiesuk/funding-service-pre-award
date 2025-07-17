from datetime import datetime

import pytest
from bs4 import BeautifulSoup

from tests.pre_award.apply_tests.api_data.test_data import TEST_APPLICATION_SUMMARIES


@pytest.fixture
def display_data():
    return {
        "funds": [
            {
                "fund_data": {"name": "Test Fund", "funding_type": "EOI", "short_name": "TF"},
                "rounds": [
                    {
                        "is_not_yet_open": False,
                        "round_details": {
                            "title": "Test Round",
                            "deadline": "2030-12-31T11:58:00",
                            "has_eligibility": False,
                            "is_expression_of_interest": False,
                            "id": "round_id",
                            "short_name": "TR",
                        },
                        "is_past_submission_deadline": False,
                        "applications": [
                            {
                                "status": "CHANGE_REQUESTED",
                                "id": "app_id",
                                "project_name": "Test Project",
                                "last_edited": datetime(2024, 12, 23, 15, 12, 51, 889247),
                            }
                        ],
                    }
                ],
            }
        ],
        "total_applications_to_display": 1,
    }


@pytest.mark.usefixtures("mock_login", "mock_get_fund_round")
def test_changes_requested_notification(apply_test_client, mocker, templates_rendered, display_data):
    mocker.patch(
        "pre_award.apply.default.account_routes.search_applications",
        return_value=TEST_APPLICATION_SUMMARIES,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.check_change_requested_for_applications",
        return_value=True,
    )
    apply_test_client.application.jinja_env.globals["get_service_title"] = lambda: "Test Service Title"

    response = apply_test_client.get("/account?fund=CTDF", follow_redirects=True)
    assert response.status_code == 200

    template, context = templates_rendered[0]
    assert template.name == "apply/dashboard_single_fund.html"

    rendered_html = template.render(display_data=display_data, change_request=True, govukRebrand=True)
    soup = BeautifulSoup(rendered_html, "html.parser")

    assert "The assessor has requested changes to your application." in soup.prettify()


@pytest.mark.usefixtures("mock_login", "mock_get_fund_round")
def test_no_changes_requested_notification(apply_test_client, mocker, templates_rendered, display_data):
    mocker.patch(
        "pre_award.apply.default.account_routes.search_applications",
        return_value=TEST_APPLICATION_SUMMARIES,
    )
    mocker.patch(
        "pre_award.apply.default.account_routes.check_change_requested_for_applications",
        return_value=False,
    )
    apply_test_client.application.jinja_env.globals["get_service_title"] = lambda: "Test Service Title"

    # Change the status to SUBMITTED
    display_data["funds"][0]["rounds"][0]["applications"][0]["status"] = "SUBMITTED"

    response = apply_test_client.get("/account?fund=CTDF", follow_redirects=True)
    assert response.status_code == 200

    template, context = templates_rendered[0]
    assert template.name == "apply/dashboard_single_fund.html"

    rendered_html = template.render(display_data=display_data, change_request=False, govukRebrand=True)
    soup = BeautifulSoup(rendered_html, "html.parser")
    assert "The assessor has requested changes to your application." not in soup.prettify()
