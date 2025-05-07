"""
Test session functionality
"""

from unittest.mock import PropertyMock, patch

import pytest

from pre_award.authenticator.security.utils import validate_token
from pre_award.config.envs.default import SafeAppConfig


@pytest.mark.usefixtures("authenticator_test_client")
@pytest.mark.usefixtures("mock_redis_magic_links")
class TestSignout:
    # TODO: Remove this file if clear_session_get and /sessions/sign-out get request is removed
    created_link_keys = []
    used_link_keys = []
    valid_token = ""

    def test_signout_checks_for_cookie(self, authenticator_test_client, mock_redis_sessions):
        """
        GIVEN a running Flask client
        WHEN we issue a GET to /sessions/sign-out
        THEN the endpoint checks for existing auth cookie
        :param authenticator_test_client:
        """
        endpoint = "/sessions/sign-out"

        response_get = authenticator_test_client.get(endpoint)
        assert response_get.status_code == 302
        assert response_get.location == "/service/magic-links/signed-out/no_token"

    def test_signout_clears_cookie(self, authenticator_test_client, mock_redis_sessions):
        """
        GIVEN a running Flask client
        WHEN we issue a GET to /sessions/sign-out
        with an existing invalid "fsd_user_token" auth cookie
        THEN the endpoint clears the cookie
        :param authenticator_test_client:
        """
        endpoint = "/sessions/sign-out"
        authenticator_test_client.set_cookie(key="fsd_user_token", value="invalid_token")
        authenticator_test_client.set_cookie(key="user_fund_and_round", value="fund_round")

        with patch("pre_award.authenticator.api.session.auth_session.validate_token") as mock_validate_token:  # noqa
            mock_validate_token.return_value = {
                "fund": "test_fund",
                "round": "test_round",
                "accountId": "test_account",
            }
            response = authenticator_test_client.get(endpoint)

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
        WHEN we issue a get to /sessions/sign-out
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
        auth_cookie = authenticator_test_client.get_cookie(key=expected_cookie_name, domain="communities.gov.localhost")

        # Check auth token cookie is set and is valid
        assert auth_cookie is not None, (
            f"Auth cookie '{expected_cookie_name}' was expected to be set, but could not be found"
        )
        self.valid_token = auth_cookie.value
        credentials = validate_token(self.valid_token)
        assert credentials.get("accountId") == expected_account_id

        # Check user can sign out
        endpoint = "/sessions/sign-out"
        response = authenticator_test_client.get(endpoint)
        assert response.status_code == 302
        assert (
            "fsd_user_token=; Domain=communities.gov.localhost; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/"
            in response.headers.get("Set-Cookie")
        )
        assert response.location == "/service/magic-links/signed-out/sign_out_request"

    def test_session_sign_out_using_correct_route_with_specified_return_app(self, authenticator_test_client, mocker):
        """
        GIVEN a running Flask client
        WHEN we issue a GET to /sessions/sign-out with return_app
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
        endpoint = f"/sessions/sign-out?return_app={return_app}"

        response = authenticator_test_client.get(endpoint)

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
        endpoint = f"/sessions/sign-out?return_app={return_app}"

        response = authenticator_test_client.get(endpoint)

        assert response.status_code == 400
        assert response.json["detail"] == "Unknown return app."

    def test_signout_retains_return_path(self, authenticator_test_client, mock_redis_sessions):
        endpoint = "/sessions/sign-out?return_app=post-award-frontend&return_path=/foo"
        response = authenticator_test_client.get(endpoint)

        assert response.status_code == 302
        assert response.location == "/service/sso/signed-out/no_token?return_app=post-award-frontend&return_path=/foo"
