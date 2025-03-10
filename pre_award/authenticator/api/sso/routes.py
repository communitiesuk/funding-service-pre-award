from urllib.parse import urlencode, urljoin, urlparse

import msal
import requests
from flask import abort, current_app, make_response, redirect, request, session
from flask.views import MethodView
from fsd_utils import clear_sentry

from pre_award.authenticator.api.session.auth_session import AuthSessionBase
from pre_award.authenticator.models.account import AccountMethods
from pre_award.common.blueprints import Blueprint
from pre_award.config import Config

api_sso_bp = Blueprint("api_sso", __name__, url_prefix="/sso")


class SsoBase:
    @staticmethod
    def _load_cache():
        cache = msal.SerializableTokenCache()
        if session.get("token_cache"):
            cache.deserialize(session["token_cache"])
        return cache

    @staticmethod
    def _save_cache(cache):
        if cache.has_state_changed:
            session["token_cache"] = cache.serialize()

    @staticmethod
    def _build_msal_app(cache=None, authority=None):
        return msal.ConfidentialClientApplication(
            Config.AZURE_AD_CLIENT_ID,
            authority=authority or Config.AZURE_AD_AUTHORITY,
            client_credential=Config.AZURE_AD_CLIENT_SECRET,
            token_cache=cache,
        )

    @staticmethod
    def _get_origin_from_url(url):
        parsed_uri = urlparse(url)
        return f"{parsed_uri.scheme}://{parsed_uri.netloc}"

    def build_auth_code_flow(self, authority=None, scopes=None):
        return self._build_msal_app(authority=authority).initiate_auth_code_flow(
            scopes or [], redirect_uri=Config.AZURE_AD_REDIRECT_URI
        )

    def _get_token_from_cache(self, scope=None):
        cache = self._load_cache()  # This web app maintains one cache per session
        cca = self._build_msal_app(cache=cache)
        accounts = cca.get_accounts()
        if accounts:  # So all account(s) belong to the current signed-in user
            result = cca.acquire_token_silent(scope, account=accounts[0])
            self._save_cache(cache)
            return result

    def logout(self, post_logout_redirect_uri=None):
        """
        Clears the user session then redirects to
        Azure AD logout endpoint to logout from our tenants web session too
        :return:
        """
        azure_ad_sign_out_url = (
            Config.AZURE_AD_AUTHORITY
            + "/oauth2/v2.0/logout"
            + ("?post_logout_redirect_uri=" + post_logout_redirect_uri if post_logout_redirect_uri else "")
        )

        # Clear session
        session.clear()
        response = make_response(redirect(azure_ad_sign_out_url), 302)

        # Clear the JWT cookie
        response.set_cookie(
            Config.FSD_USER_TOKEN_COOKIE_NAME,
            "",
            domain=Config.COOKIE_DOMAIN,
            expires=0,
        )

        # Clear any additional session state (e.g., Sentry)
        clear_sentry()
        return response


class SsoLoginView(SsoBase, MethodView):
    def get(self):
        """
        GET /sso/login endpoint
        Redirects to the Azure AD auth uri
        :return: 302 redirect to Microsoft Login
        """
        session["flow"] = self.build_auth_code_flow(scopes=Config.MS_GRAPH_PERMISSIONS_SCOPE)

        if return_app := request.args.get("return_app"):
            session["return_app"] = return_app
            session["return_path"] = request.args.get("return_path")
            current_app.logger.debug(
                "Setting return app to %(return_app)s for this session", dict(return_app=return_app)
            )

        return redirect(session["flow"]["auth_uri"]), 302


class SsoLogoutView(SsoBase, MethodView):
    # Deprecation warning (Use logout_post instead)
    def get(self):
        """GET /sso/logout endpoint"""
        post_logout_redirect_uri = request.args.get(
            "post_logout_redirect_uri",
            Config.SSO_POST_SIGN_OUT_URL + f"?{urlencode({'return_app': session['return_app']})}"
            if "return_app" in session
            else "",
        )
        return self.logout(post_logout_redirect_uri)

    def post(self):
        """POST /sso/logout endpoint"""
        post_logout_redirect_uri = request.form.get(
            "post_logout_redirect_uri",
            Config.SSO_POST_SIGN_OUT_URL + f"?{urlencode({'return_app': session['return_app']})}"
            if "return_app" in session
            else "",
        )
        return self.logout(post_logout_redirect_uri)


class SsoGetTokenView(SsoBase, MethodView):
    def get(self):
        """
        GET /sso/get-token
        The endpoint that Azure AD redirects back to
        after successful authentication.
        Validates args from return request and if claims validated,
        then creates a user property on the session with token claims
        # NOTE: The absolute URL that points here must match
        # this app's redirect_uri set in Azure AD
        :return: 200 json of valid user token claims or 404 on error
        """
        try:
            cache = self._load_cache()
            result = self._build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
                session.get("flow", {}), request.args
            )
            if "error" in result:
                return abort(500, "Azure AD get-token flow failed with: {}".format(result))
            session["user"] = result.get("id_token_claims")
            self._save_cache(cache)
        except ValueError as e:  # Usually caused by CSRF
            current_app.logger.warning("Value Error on get_token route: %(error)s", dict(error=str(e)))

        if "user" not in session or not session["user"].get("sub"):
            return {"message": "No valid token"}, 404

        updated_account = AccountMethods.create_or_update_account(
            azure_ad_subject_id=session["user"].get("sub"),
            email=session["user"].get("preferred_username"),
            full_name=session["user"].get("name"),
            roles=session["user"].get("roles") or [],
        )

        redirect_url = urljoin(  # TODO: Remove defaulting to Assessment, instead use return_app
            Config.ASSESSMENT_FRONTEND_HOST, "/assess/fund_dashboard"
        )
        if return_app := session.get("return_app"):
            if safe_app := Config.SAFE_RETURN_APPS.get(return_app):
                if return_path := session.get("return_path"):
                    redirect_url = self._get_origin_from_url(safe_app.login_url) + return_path
                else:
                    redirect_url = safe_app.login_url

                current_app.logger.info(
                    "Returning to %(return_app)s @ %(redirect_url)s",
                    dict(return_app=return_app, redirect_url=redirect_url),
                )
            else:
                current_app.logger.warning("%(return_app)s not listed as a safe app.", dict(return_app=return_app))
                resp = make_response({"detail": "Unknown return app."}, 400)
                resp.headers["Content-Type"] = "application/json"
                return resp

        # Create session token, set cookie and redirect
        return AuthSessionBase.create_session_and_redirect(
            account=updated_account,
            redirect_url=redirect_url,
            is_via_magic_link=False,
            timeout_seconds=Config.FSD_ASSESSMENT_SESSION_TIMEOUT_SECONDS,
        )


class SsoGraphCallView(SsoBase, MethodView):
    def get(self):
        """
        GET /sso/graph-call endpoint
        Shows the graph object for the current authenticated user
        Requires a valid token in the session
        :return: 200 json of user graph data or 404 not found
        """
        token = self._get_token_from_cache(Config.MS_GRAPH_PERMISSIONS_SCOPE)
        if not token:
            return {"message": "No valid token"}, 404
        graph_data = requests.get(  # Use token to call downstream service
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": "Bearer " + token["access_token"]},
        ).json()
        return graph_data, 200


api_sso_bp.add_url_rule("/login", view_func=SsoLoginView.as_view("login"))
api_sso_bp.add_url_rule("/logout", view_func=SsoLogoutView.as_view("logout"))
api_sso_bp.add_url_rule("/get-token", view_func=SsoGetTokenView.as_view("get_token"))
api_sso_bp.add_url_rule("/graph-call", view_func=SsoGraphCallView.as_view("graph_call"))
