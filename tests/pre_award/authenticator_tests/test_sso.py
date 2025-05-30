import pytest
from flask import session
from fsd_utils.authentication.utils import validate_token_rs256

from tests.pre_award.authenticator_tests.testing.mocks.mocks.msal import (
    ConfidentialClientApplication,
    HijackedConfidentialClientApplication,
    RolelessConfidentialClientApplication,
    expected_fsd_user_token_claims,
    id_token_claims,
)


def test_sso_login_redirects_to_ms(authenticator_test_client):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/login
    THEN we should be redirected to Microsoft Login
    """
    endpoint = "/sso/login"
    expected_redirect = "https://login.microsoftonline.com/"
    response = authenticator_test_client.get(endpoint)

    assert response.status_code == 302
    assert response.location.startswith(expected_redirect) is True


def test_sso_login_sets_return_app_in_session(authenticator_test_client):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/login
    THEN we should be redirected to Microsoft Login
    """
    return_app = "post-award-frontend"

    endpoint = f"/sso/login?return_app={return_app}"
    authenticator_test_client.get(endpoint)
    assert session.get("return_app") == return_app


def test_sso_login_sets_return_path_in_session(authenticator_test_client):
    return_app = "post-award-frontend"

    endpoint = f"/sso/login?return_app={return_app}&return_path=/foo"
    authenticator_test_client.get(endpoint)
    assert session.get("return_path") == "/foo"


# TODO: Remove this test if logout_get and /sso/logout get request is removed
def test_get_sso_logout_redirects_to_ms(authenticator_test_client):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/logout
    THEN we should be redirected to Microsoft Logout
    """
    endpoint = "/sso/logout"
    expected_redirect = "https://login.microsoftonline.com/organizations/oauth2/v2.0/logout"
    response = authenticator_test_client.get(endpoint)

    assert response.status_code == 302
    assert response.location.startswith(expected_redirect) is True


# TODO: Remove this test if logout_get and /sso/logout get request is removed
def test_get_sso_logout_redirect_contains_return_app(authenticator_test_client, mock_redis_sessions):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/logout with return_app
        set
    THEN we should be redirected to Microsoft Logout
    AND then be redirected back with the correct
        query string for that return_app
    """
    endpoint = "/sso/logout"

    with authenticator_test_client.session_transaction() as test_session:
        test_session["return_app"] = "post-award-frontend"

    expected_post_logout_redirect = "return_app=post-award-frontend"

    response = authenticator_test_client.get(endpoint)

    assert response.status_code == 302
    assert response.location.endswith(expected_post_logout_redirect) is True


def test_sso_logout_redirects_to_ms(authenticator_test_client):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a POST request for /sso/logout
    THEN we should be redirected to Microsoft Logout
    """
    endpoint = "/sso/logout"
    expected_redirect = "https://login.microsoftonline.com/organizations/oauth2/v2.0/logout"
    response = authenticator_test_client.post(endpoint)

    assert response.status_code == 302
    assert response.location.startswith(expected_redirect) is True


def test_sso_logout_redirect_contains_return_app(authenticator_test_client, mock_redis_sessions):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a POST request for /sso/logout with return_app
        set
    THEN we should be redirected to Microsoft Logout
    AND then be redirected back with the correct
        query string for that return_app
    """
    endpoint = "/sso/logout"

    with authenticator_test_client.session_transaction() as test_session:
        test_session["return_app"] = "post-award-frontend"

    expected_post_logout_redirect = "return_app=post-award-frontend"

    response = authenticator_test_client.post(endpoint)

    assert response.status_code == 302
    assert response.location.endswith(expected_post_logout_redirect) is True


@pytest.mark.filterwarnings("ignore:Value Error on get_token route:UserWarning")
def test_sso_get_token_returns_404(authenticator_test_client):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/get-token
    THEN we should receive a 404 "No valid token" message
    """
    endpoint = "/sso/get-token"

    response = authenticator_test_client.get(endpoint)

    assert response.status_code == 404
    assert response.get_json()["message"] == "No valid token"


def test_sso_get_token_sets_session_and_redirects(authenticator_test_client, mock_msal_client_application):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/get-token with a valid
        response from azure_ad via the mock_msal_client_application
    THEN we should receive a 302 redirect response with
        the correct claims in the session
    """
    endpoint = "/sso/get-token"
    response = authenticator_test_client.get(endpoint)

    assert response.status_code == 302
    assert session.get("user") == id_token_claims


def test_sso_get_token_prevents_overwrite_of_existing_azure_subject_id(authenticator_test_client, mocker, caplog):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/get-token with a valid
        response from azure_ad via the mock_msal_client_application
    THEN we should receive a 302 redirect response with
        the correct claims in the session
    """
    mocker.patch(
        "msal.ConfidentialClientApplication.acquire_token_by_auth_code_flow",
        ConfidentialClientApplication.acquire_token_by_auth_code_flow,
    )
    endpoint = "/sso/get-token"
    response = authenticator_test_client.get(endpoint)

    assert response.status_code == 302
    assert session.get("user") == id_token_claims

    mocker.patch(
        "msal.ConfidentialClientApplication.acquire_token_by_auth_code_flow",
        HijackedConfidentialClientApplication.acquire_token_by_auth_code_flow,
    )

    endpoint = "/sso/get-token"
    error_response = authenticator_test_client.get(endpoint)

    assert error_response.status_code == 500
    assert (
        "Cannot update account id: usersso - "
        "attempting to update existing azure_ad_subject_id "
        "from abc to xyx which is not allowed." in caplog.text
    )


def test_sso_get_token_500_when_error_in_auth_code_flow(authenticator_test_client, mocker, caplog):
    mock_build_msal_app = mocker.patch("pre_award.authenticator.api.sso.routes.SsoBase._build_msal_app")
    mock_msal_app = mock_build_msal_app.return_value
    mock_msal_app.acquire_token_by_auth_code_flow.return_value = {"error": "some_error"}

    endpoint = "/sso/get-token"
    response = authenticator_test_client.get(endpoint)

    assert response.status_code == 500
    assert "some_error" not in response.text


def test_sso_get_token_logs_error_for_roleless_users(authenticator_test_client, mocker, caplog):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/get-token with a valid
        response from azure_ad via the mock_msal_client_application
    THEN we should receive a 302 redirect response with
        the correct claims in the session
    """
    mocker.patch(
        "msal.ConfidentialClientApplication.acquire_token_by_auth_code_flow",
        RolelessConfidentialClientApplication.acquire_token_by_auth_code_flow,
    )

    endpoint = "/sso/get-token"
    error_response = authenticator_test_client.get(endpoint)

    assert error_response.status_code == 302


def test_sso_get_token_sets_expected_fsd_user_token_cookie_claims(
    authenticator_test_client, mock_msal_client_application
):
    """
    Args:
        authenticator_test_client:
        mock_msal_client_application:

    Returns:

    """
    endpoint = "/sso/get-token"
    expected_cookie_name = "fsd_user_token"

    response = authenticator_test_client.get(endpoint)
    assert response.status_code == 302
    auth_cookie = authenticator_test_client.get_cookie(key=expected_cookie_name, domain="communities.gov.localhost")

    # Check auth token cookie is set and is valid
    assert auth_cookie is not None, (
        f"Auth cookie '{expected_cookie_name}' was expected to be set, but could not be found"
    )
    valid_token = auth_cookie.value
    credentials = validate_token_rs256(valid_token)
    assert credentials.get("accountId") == expected_fsd_user_token_claims.get("accountId")
    assert credentials.get("azureAdSubjectId") == expected_fsd_user_token_claims.get("azureAdSubjectId")
    assert credentials.get("email") == expected_fsd_user_token_claims.get("email")
    assert credentials.get("fullName") == expected_fsd_user_token_claims.get("fullName")


def test_sso_get_token_redirects_to_return_app_login_url(
    authenticator_test_client, mock_msal_client_application, mock_redis_sessions
):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/get-token with a valid
        response from azure_ad via the mock_msal_client_application
        with a VALID return app set in the session
    THEN we should receive a 302 redirect response with
        the correct location to the return_app
    """
    endpoint = "/sso/get-token"

    with authenticator_test_client.session_transaction() as test_session:
        test_session["return_app"] = "post-award-frontend"

    response = authenticator_test_client.get(endpoint)

    assert response.location == "https://find-monitoring-data.communities.gov.localhost:4001/"


def test_sso_get_token_redirects_to_return_app_host_with_request_path(
    authenticator_test_client, mock_msal_client_application, mock_redis_sessions
):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/get-token with a valid
        response from azure_ad via the mock_msal_client_application
        with a VALID return app set in the session
    THEN we should receive a 302 redirect response with
        the correct location to the return_app
    """
    endpoint = "/sso/get-token"

    with authenticator_test_client.session_transaction() as test_session:
        test_session["return_app"] = "post-award-frontend"
        test_session["return_path"] = "/foo"

    response = authenticator_test_client.get(endpoint)

    assert response.location == "https://find-monitoring-data.communities.gov.localhost:4001/foo"


def test_sso_get_token_400_abort_with_invalid_return_app(
    authenticator_test_client, mock_msal_client_application, mock_redis_sessions
):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/get-token with a valid
        response from azure_ad via the mock_msal_client_application
        with an INVALID return app set in the session
    THEN we should receive a 400 response with the correct
        message
    """
    endpoint = "/sso/get-token"

    with authenticator_test_client.session_transaction() as test_session:
        test_session["return_app"] = "invalid-return-app"

    response = authenticator_test_client.get(endpoint)

    assert response.status_code == 400
    assert response.json["detail"] == "Unknown return app."


def test_sso_graphcall_returns_404(authenticator_test_client, mock_redis_sessions):
    """
    GIVEN We have a functioning Authenticator API
    WHEN a GET request for /sso/graphcall
    THEN we should be redirected to Microsoft Login
    """
    endpoint = "/sso/graph-call"
    response = authenticator_test_client.get(endpoint)

    assert response.status_code == 404
    assert response.get_json()["message"] == "No valid token"
