import pytest
from bs4 import BeautifulSoup

from pre_award.config import Config


@pytest.mark.parametrize(
    "url, expected_service_desk_link, expected_title",
    [
        (
            "/contact_us?fund=bad&round=bad",
            Config.SUPPORT_DESK_APPLY,
            "Contact us if you have any questions.",
        ),
        (
            "/contact_us",
            Config.SUPPORT_DESK_APPLY,
            "Contact us if you have any questions.",
        ),
    ],
)
def test_contact_us_portal(apply_test_client, url, expected_service_desk_link, expected_title):
    response = apply_test_client.get(url)

    soup = BeautifulSoup(response.data, "html.parser")

    assert any("Please contact us through our" in h3.text for h3 in soup.find_all("h3", class_="govuk-heading-s"))
    assert len(soup.find_all("a", href=expected_service_desk_link)) == 1
    assert len(soup.find_all("p", string=lambda text: expected_title in text if text else False)) == 1


@pytest.mark.parametrize(
    "url, expected_status, expected_redirect",
    [
        ("/privacy?fund=cof&round=r3w1", 302, "http://privacy.com"),
        ("/privacy?fund=bad&round=r3w1", 404, None),
        ("/privacy?fund=cof&round=bad", 302, "http://privacy.com"),
    ],
)
def test_privacy(apply_test_client, url, expected_status, expected_redirect):
    response = apply_test_client.get(url, follow_redirects=False)
    assert response.status_code == expected_status
    assert response.location == expected_redirect


@pytest.mark.parametrize(
    "url, expected_status, expected_redirect",
    [
        ("/feedback?fund=cof&round=r3w1", 302, "http://feedback.com"),
        (
            "/feedback?fund=bad&round=r3w1",
            302,
            "/contact_us?fund=bad&round=r3w1",
        ),
        ("/feedback?fund=cof&round=bad", 302, "http://feedback.com"),
    ],
)
def test_feedback(apply_test_client, url, expected_status, expected_redirect):
    response = apply_test_client.get(url, follow_redirects=False)
    assert response.status_code == expected_status
    assert response.location == expected_redirect
