from types import SimpleNamespace

import pytest
from bs4 import BeautifulSoup

from pre_award.apply.default.data import RoundStatus
from tests.pre_award.apply_tests.api_data.test_data import TEST_APPLICATIONS

TEST_APPLICATION_EN = TEST_APPLICATIONS[0]


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
        "pre_award.apply.default.application_routes.get_change_request_field_ids",
        return_value=[],
    )
    mocker.patch(
        "pre_award.apply.default.application_routes.get_application_display_config",
        return_value=[
            SimpleNamespace(
                section_id="sec-1",
                id="sec-1",
                title="Test Section",
                weighting=0,
                requires_feedback=False,
                show_in_tasklist=True,
                children=[],
            )
        ],
    )


def _make_stub_round(privacy):
    return SimpleNamespace(
        id="test-round-id",
        short_name="r2w3",
        fund_short_name="COF",
        privacy_notice=privacy,
        title="r2w3",
        deadline="2050-01-01T00:00:01",
    )


def test_tasklist_shows_privacy_section_when_round_has_privacy(
    apply_test_client, mocker, mock_login, mock_applications
):
    stub_round = _make_stub_round("https://example.com/privacy")
    stub_fund = SimpleNamespace(short_name="COF")
    mocker.patch("app.find_fund_and_round_in_request", return_value=(stub_fund, stub_round))

    response = apply_test_client.get("tasklist/test-application-id", follow_redirects=True)
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")

    heading = soup.find("h2", string=lambda s: s and "How we'll use your information" in s)
    assert heading is not None

    # privacy link present and points to stub URL
    link = soup.find("a", class_="govuk-link", string=lambda s: s and "privacy notice" in s.lower())
    assert link is not None
    assert link.get("href") == "https://example.com/privacy"


def test_tasklist_hides_privacy_section_when_round_has_no_privacy(
    apply_test_client, mocker, mock_login, mock_applications
):
    stub_round = _make_stub_round("")
    stub_fund = SimpleNamespace(short_name="COF")
    mocker.patch("app.find_fund_and_round_in_request", return_value=(stub_fund, stub_round))

    response = apply_test_client.get("tasklist/test-application-id", follow_redirects=True)
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")

    # assert that heading and privacy link not present
    heading = soup.find("h2", string=lambda s: s and "How we'll use your information" in s)
    assert heading is None

    link = soup.find("a", class_="govuk-link", string=lambda s: s and "privacy notice" in s.lower())
    assert link is None
