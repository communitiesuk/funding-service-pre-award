import pytest


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
