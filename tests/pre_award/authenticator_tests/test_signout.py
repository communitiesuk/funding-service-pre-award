"""
Test session functionality
"""

from unittest.mock import PropertyMock, patch

import pytest
from bs4 import BeautifulSoup

from pre_award.authenticator.security.utils import create_token, validate_token
from pre_award.config.envs.default import SafeAppConfig


@pytest.mark.usefixtures("authenticator_test_client")
@pytest.mark.usefixtures("mock_redis_magic_links")
class TestSignout:
    created_link_keys = []
    used_link_keys = []
    valid_token = ""

    def test_signout_checks_for_cookie(self, authenticator_test_client, mock_redis_sessions):
        """
        GIVEN a running Flask client
        WHEN we issue a POST to /sessions/sign-out
        THEN the endpoint checks for existing auth cookie
        :param authenticator_test_client:
        """
        endpoint = "/sessions/sign-out"

        response_post = authenticator_test_client.post(endpoint)
        assert response_post.status_code == 302
        assert response_post.location == "/service/magic-links/signed-out/no_token"

    def test_signout_clears_cookie(self, authenticator_test_client, mock_redis_sessions):
        """
        GIVEN a running Flask client
        WHEN we issue a POST to /sessions/sign-out
        with an existing invalid "fsd_user_token" auth cookie
        THEN the endpoint clears the cookie
        :param authenticator_test_client:
        """
        endpoint = "/sessions/sign-out"
        authenticator_test_client.set_cookie("fsd_user_token", "invalid_token")
        authenticator_test_client.set_cookie("user_fund_and_round", "fund_round")

        with patch("pre_award.authenticator.api.session.auth_session.validate_token") as mock_validate_token:  # noqa
            mock_validate_token.return_value = {
                "fund": "test_fund",
                "round": "test_round",
                "accountId": "test_account",
            }

            response = authenticator_test_client.post(endpoint)

            assert response.status_code == 302
            assert (
                "fsd_user_token=; Domain=communities.gov.localhost; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/"
                in response.headers.get(  # noqa
                    "Set-Cookie"
                )
            )
            assert (
                response.location == "/service/magic-links/signed-out/sign_out_request?fund=test_fund&round=test_round"  # noqa
            )

    def test_magic_link_auth_can_be_signed_out(
        self,
        mocker,
        authenticator_test_client,
        mock_redis_sessions,
        create_magic_link,
        mock_get_applications_for_account,
    ):
        """
        GIVEN a running Flask client, redis instance and
        and a valid magic link has been clicked and a valid
        jwt auth token set
        WHEN we issue a POST to /sessions/sign-out
        THEN the token is cleared and the user signed out
        :param authenticator_test_client:
        """
        expected_account_id = "usera"
        expected_cookie_name = "fsd_user_token"
        link_key = create_magic_link
        self.created_link_keys.append(link_key)
        use_endpoint = f"/magic-links/{link_key}"
        authenticator_test_client.get(use_endpoint)
        self.used_link_keys.append(link_key)
        auth_cookie = authenticator_test_client.get_cookie(expected_cookie_name, "communities.gov.localhost")

        # Check auth token cookie is set and is valid
        assert auth_cookie is not None, (
            f"Auth cookie '{expected_cookie_name}' was expected to be set, but could not be found"
        )
        self.valid_token = auth_cookie.value
        credentials = validate_token(self.valid_token)
        assert credentials.get("accountId") == expected_account_id

        # Check user can sign out
        endpoint = "/sessions/sign-out"
        response = authenticator_test_client.post(endpoint)
        assert response.status_code == 302
        assert (
            "fsd_user_token=; Domain=communities.gov.localhost; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/"
            in response.headers.get("Set-Cookie")
        )
        assert response.location == "/service/magic-links/signed-out/sign_out_request"

    def test_user_page_for_logged_out_user(self, authenticator_test_client):
        """
        GIVEN a running Flask client and user is not logged in
        WHEN we access the user page
        THEN the user page is displayed
        :param authenticator_test_client:
        """
        endpoint = "/service/user"
        response = authenticator_test_client.get(endpoint)
        assert response.status_code == 200
        assert """<p class="govuk-body">You are not logged in.</p>""" in response.get_data(as_text=True)
        assert (
            """<a href="/sso/login" role="button" draggable="false" class="govuk-button" data-module="govuk-button">\n  Sign in\n</a>"""  # noqa
            in response.get_data(as_text=True)
        )

    def test_user_page_with_missing_roles(self, authenticator_test_client):
        """
        GIVEN a running Flask client, user is logged in but does not
        have the required roles
        WHEN we access the user page
        THEN the roles required error is shown on the user page
        :param authenticator_test_client:
        """

        test_payload = {
            "accountId": "test-user",
            "email": "test@example.com",
            "fullName": "Test User",
            "roles": ["COF_LEAD_ASSESSOR", "COF_ASSESSOR", "COF_COMMENTER"],
        }

        token = create_token(test_payload)
        authenticator_test_client.set_cookie(key="fsd_user_token", value=token)

        endpoint = "/service/user?roles_required=ultimate_assessor|mega_assessor"
        response = authenticator_test_client.get(endpoint)
        assert response.status_code == 403
        assert (
            """<p class="govuk-body">You do not have access as your account does not have the right permissions set up."""  # noqa
            in response.get_data(as_text=True)
        )
        assert """<p class="govuk-body">Please contact us through our support desk portal""" in response.get_data(
            as_text=True
        )  # noqa
        assert (
            """<a href="/sso/login" role="button" draggable="false" class="govuk-button" data-module="govuk-button">\n  Sign in\n</a>"""  # noqa
            not in response.get_data(as_text=True)
        )

    def test_user_page_with_correct_roles(self, authenticator_test_client):
        """
        GIVEN a running Flask client, user is logged in and
        has the required roles
        WHEN we access the user page
        THEN the user page is displayed with option to sign out
        :param authenticator_test_client:
        """

        test_payload = {
            "accountId": "test-user",
            "email": "test@example.com",
            "fullName": "Test User",
            "roles": ["COF_LEAD_ASSESSOR", "COF_ASSESSOR", "COF_COMMENTER"],
        }

        token = create_token(test_payload)
        authenticator_test_client.set_cookie(key="fsd_user_token", value=token)

        endpoint = "/service/user?roles_required=cof_assessor|cof_commenter"
        response = authenticator_test_client.get(endpoint)
        assert response.status_code == 200
        assert (
            """<a href="/sso/logout" role="button" draggable="false" class="govuk-button" data-module="govuk-button">\n  Sign out\n</a>"""  # noqa
            in response.get_data(as_text=True)
        )

    def test_session_sign_out_using_correct_route_with_specified_return_app(self, authenticator_test_client, mocker):
        """
        GIVEN a running Flask client
        WHEN we issue a POST to /sessions/sign-out with return_app
            query param set to a valid value
        THEN the endpoint modifies the redirect_route to the value
            specified in the SAFE_RETURN_APPS config
        :param authenticator_test_client:
        """
        mocker.patch(
            "pre_award.config.Config.SAFE_RETURN_APPS",
            new_callable=PropertyMock,
            return_value={
                "test-app": SafeAppConfig(
                    login_url="testapp.gov.uk/login",
                    logout_endpoint="sso_bp.signed_out",
                    service_title="Test Application",
                )
            },
        )

        return_app = "test-app"
        data = {"return_app": return_app}
        endpoint = f"/sessions/sign-out?return_app={return_app}"

        response = authenticator_test_client.post(endpoint, data=data)

        assert response.status_code == 302
        assert response.location == "/service/sso/signed-out/no_token?return_app=test-app"

    def test_session_sign_out_abort_400_if_invalid_return_app_is_set(self, authenticator_test_client):
        """
        GIVEN a running Flask client
        WHEN we issue a GET to /sessions/sign-out with return_app
            query param set to an invalid value
        THEN the endpoint returns a 400 error with the correct
            message
        :param authenticator_test_client:
        """
        return_app = "invalid-return-app"
        data = {"return_app": return_app}
        endpoint = f"/sessions/sign-out?return_app={return_app}"

        response = authenticator_test_client.post(endpoint, data=data)

        assert response.status_code == 400
        assert response.json["detail"] == "Unknown return app."

    def test_sign_out_template_service_title_is_dynamic(self, authenticator_test_client, mocker):
        """
        GIVEN a running Flask client
        WHEN we issue a GET to /service/sso/signed-out with return_app
            query param set to a valid value
        THEN the template should contain the correct service name
        :param authenticator_test_client:
        """
        mocker.patch(
            "pre_award.config.Config.SAFE_RETURN_APPS",
            new_callable=PropertyMock,
            return_value={
                "test-app": SafeAppConfig(
                    login_url="testapp.gov.uk/login",
                    logout_endpoint="sso_bp.signed_out",
                    service_title="Test Application",
                )
            },
        )

        return_app = "test-app"
        endpoint = f"/service/sso/signed-out/no_token?return_app={return_app}"

        response = authenticator_test_client.get(endpoint)

        page_html = BeautifulSoup(response.data, "html.parser")
        assert response.status_code == 200
        assert "Test Application" in str(page_html)

    def test_sign_out_template_service_title_defaults_to_access_funding(
        self,
        authenticator_test_client,
    ):
        """
        GIVEN a running Flask client
        WHEN we issue a GET to /service/sso/signed-out without a return_app being set
        THEN the template should contain the correct default value "Access Funding"
        :param authenticator_test_client:
        """
        endpoint = "/service/sso/signed-out/no_token"

        response = authenticator_test_client.get(endpoint)

        page_html = BeautifulSoup(response.data, "html.parser")
        assert response.status_code == 200
        assert "Access Funding" in str(page_html)

    def test_signout_retains_return_path(self, authenticator_test_client, mock_redis_sessions):
        data = {"return_app": "post-award-frontend", "return_path": "/foo"}
        endpoint = "/sessions/sign-out"
        response = authenticator_test_client.post(endpoint, data=data)

        assert response.status_code == 302
        assert response.location == "/service/sso/signed-out/no_token?return_app=post-award-frontend&return_path=/foo"
