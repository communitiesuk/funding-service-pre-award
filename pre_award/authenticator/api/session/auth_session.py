from datetime import datetime, timedelta
from typing import TYPE_CHECKING

import jwt
from flask import current_app, make_response, redirect, request, session, url_for
from flask.views import MethodView
from fsd_utils import clear_sentry

from pre_award.authenticator.api.responses import error_response
from pre_award.authenticator.api.session.exceptions import SessionCreateError
from pre_award.authenticator.models.magic_link import MagicLinkMethods
from pre_award.authenticator.security.utils import create_token, decode_with_options, validate_token
from pre_award.common.blueprints import Blueprint
from pre_award.config import Config

if TYPE_CHECKING:
    from pre_award.authenticator.models.account import Account as Account


api_sessions_bp = Blueprint("api_sessions", __name__)


class AuthSessionBase:
    @staticmethod
    def clear_session(return_app=None, return_path=None):
        """
        Clears the user session (signing them out)
        Also deletes an existing jwt auth cookie and removes the corresponding
        link records from redis

        Returns: 302 redirect to signed-out page
        """
        fund_short_name = None
        round_short_name = None
        existing_auth_token = request.cookies.get(Config.FSD_USER_TOKEN_COOKIE_NAME)
        existing_fund_round_token = request.cookies.get(Config.FSD_FUND_AND_ROUND_COOKIE_NAME)
        status = "no_token"
        valid_token = False
        if existing_fund_round_token:
            fund_round_token = validate_token(existing_fund_round_token)
            fund_short_name = fund_round_token.get("fund")
            round_short_name = fund_round_token.get("round")

        if existing_auth_token:
            # Check if token is valid
            try:
                valid_token = validate_token(existing_auth_token)
                status = "sign_out_request"
            except jwt.ExpiredSignatureError:
                valid_token = decode_with_options(existing_auth_token, options={"verify_exp": False})
                status = "expired_token"
            except jwt.PyJWTError as e:
                current_app.logger.warning(
                    "PyJWTError: %(error_name)s - %(error)s", dict(error_name=e.__class__.__name__, error=str(e))
                )
                status = "invalid_token"

            # If validly issued token: create query params for signout url,
            # and clear the redis store of the account and link record
            if valid_token and isinstance(valid_token, dict):
                MagicLinkMethods().clear_existing_user_record(valid_token.get("accountId"))

        # Clear the session
        session.clear()
        clear_sentry()

        redirect_route = "magic_links_bp.signed_out"  # TODO: Remove defaulting to Magic Links, instead use return_app
        if return_app:
            if safe_app := Config.SAFE_RETURN_APPS.get(return_app):
                redirect_route = safe_app.logout_endpoint
                current_app.logger.info(
                    "Returning to %(return_app)s using %(redirect_route)s",
                    dict(return_app=return_app, redirect_route=redirect_route),
                )
            else:
                current_app.logger.warning("%(return_app)s not listed as a safe app.", dict(return_app=return_app))
                resp = make_response({"detail": "Unknown return app."}, 400)
                resp.headers["Content-Type"] = "application/json"
                return resp

        # Clear the cookie and redirect to signed out page
        signed_out_url = url_for(
            redirect_route,
            status=status,
            fund=fund_short_name,
            round=round_short_name,
            return_app=return_app,
            return_path=return_path,
        )
        response = make_response(redirect(signed_out_url), 302)
        response.set_cookie(
            Config.FSD_USER_TOKEN_COOKIE_NAME,
            "",
            domain=Config.COOKIE_DOMAIN,
            expires=0,
        )
        return response

    @classmethod
    def create_session_and_redirect(
        cls,
        account: "Account",
        redirect_url: str,
        is_via_magic_link: bool,
        timeout_seconds: int = Config.FSD_SESSION_TIMEOUT_SECONDS,
        fund: str = None,
        round: str = None,
    ):
        """
        Sets a user session token in the client for a given account_id
        and then redirects to a given url
        :param account: The account object of the user we are authenticating
        :param redirect_url: The url to redirect them to after session creation
        :param timeout_seconds: (int, optional)
        The session TTL to set in seconds
        :return: 302 redirect
        """
        try:
            # session details for fsd_user_token
            fsd_user_token_session_details = cls.create_session_details_with_token(
                account,
                is_via_magic_link,
                timeout_seconds=timeout_seconds,
            )
            # session details for user's fund and round
            fund_and_round_session_details = cls.create_session_details_with_fund_and_round(
                fund=fund,
                round=round,
            )

            response = make_response(redirect(redirect_url), 302)

            # fsd_user_token cookie
            fsd_user_token_expiry = datetime.now() + timedelta(seconds=timeout_seconds)
            response.set_cookie(
                Config.FSD_USER_TOKEN_COOKIE_NAME,
                fsd_user_token_session_details["token"],
                domain=Config.COOKIE_DOMAIN,
                expires=fsd_user_token_expiry,
                secure=Config.SESSION_COOKIE_SECURE,
                samesite=Config.FSD_USER_TOKEN_COOKIE_SAMESITE,
                httponly=Config.SESSION_COOKIE_HTTPONLY,
            )
            # user_fund _and_round cookie
            fund_round_token_expiry = datetime.now() + timedelta(days=365)
            response.set_cookie(
                Config.FSD_FUND_AND_ROUND_COOKIE_NAME,
                fund_and_round_session_details["token"],
                domain=Config.COOKIE_DOMAIN,
                expires=fund_round_token_expiry,
                secure=Config.SESSION_COOKIE_SECURE,
                samesite=Config.FSD_USER_TOKEN_COOKIE_SAMESITE,
                httponly=Config.SESSION_COOKIE_HTTPONLY,
            )
            current_app.logger.info("User logged in to account : %(account_id)s", dict(account_id=account.id))
            return response
        except SessionCreateError as e:
            error_response(404, str(e))

    @classmethod
    def create_session_details_with_token(
        cls,
        account: "Account",
        is_via_magic_link: bool,
        timeout_seconds: int = Config.FSD_SESSION_TIMEOUT_SECONDS,
    ):
        """
        Creates a signed session token for the given account with appropriate roles.

        In development with debug user enabled, magic link sessions receive the debug user's
        roles to enable seamless switching between Apply and Assess workflows. In production,
        magic link users receive limited roles based on the ALLOW_ASSESSMENT_LOGIN_VIA_MAGIC_LINK
        setting to maintain security separation between applicants and assessors.
        """
        is_development_with_debug_user = (
            Config.FLASK_ENV == "development" and hasattr(Config, "DEBUG_USER_ON") and Config.DEBUG_USER_ON
        )

        if is_development_with_debug_user:
            roles = Config.DEBUG_USER.get("roles", [])
        else:
            roles = [] if is_via_magic_link and not Config.ALLOW_ASSESSMENT_LOGIN_VIA_MAGIC_LINK else account.roles

        session_details = {
            "accountId": account.id,
            "azureAdSubjectId": account.azure_ad_subject_id,
            "email": account.email,
            "fullName": account.full_name,
            "roles": roles,
            "iat": int(datetime.now().timestamp()),
            "exp": int(datetime.now().timestamp() + timeout_seconds),
        }

        session_details.update({"token": create_token(session_details)})
        session.update(session_details)
        return session_details

    @classmethod
    def create_session_details_with_fund_and_round(
        cls,
        fund: str,
        round: str,
    ):
        """
        Creates a signed expiring session token for the given account
        :param account: The account object for the user to create a token for
        :param timeout_seconds: The length of the token expiry (or timeout)
        :return: A dict including the signed session token
        """
        session_details = {
            "fund": fund,
            "round": round,
        }

        session_details.update({"token": create_token(session_details)})
        session.update(session_details)
        return session_details


class AuthSessionSignOutView(AuthSessionBase, MethodView):
    """
    Views for session related operations
    """

    # Deprecation warning (Use clear_session_post instead)
    def get(self):
        """GET /sessions/sign-out endpoint"""
        return_app = request.args.get("return_app")
        return_path = request.args.get("return_path")
        return self.clear_session(return_app, return_path)

    def post(self):
        """POST /sessions/sign-out endpoint"""
        return_app = request.form.get("return_app")
        return_path = request.form.get("return_path")
        return self.clear_session(return_app, return_path)


class AuthSessionUserView(AuthSessionBase, MethodView):
    def get(self):
        """
        GET /sessions/user endpoint
        Shows the user details of the current user session
        or an error if no authenticated user session found
        :return: 200 user details json or 404 error
        """
        token = request.cookies.get(Config.FSD_USER_TOKEN_COOKIE_NAME)
        if token:
            try:
                valid_token = validate_token(token)
                return make_response(valid_token), 200
            except jwt.PyJWTError:
                error_response(404, "Session token expired or invalid")
        error_response(404, "No session token found")


api_sessions_bp.add_url_rule("/sessions/user", view_func=AuthSessionUserView.as_view("user"))
api_sessions_bp.add_url_rule("/sessions/sign-out", view_func=AuthSessionSignOutView.as_view("sign_out"))
