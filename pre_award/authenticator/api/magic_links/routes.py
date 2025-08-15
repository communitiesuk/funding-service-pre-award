import json
from datetime import datetime
from urllib.parse import urlencode, urljoin

from flask import current_app, g, redirect, request, url_for
from flask.views import MethodView
from fsd_utils.authentication.decorators import login_requested

from pre_award.apply.default.data import get_applications_for_account
from pre_award.authenticator.api.session.auth_session import AuthSessionBase
from pre_award.authenticator.models.account import AccountMethods
from pre_award.authenticator.models.data import get_round_data
from pre_award.authenticator.models.fund import FundMethods
from pre_award.authenticator.models.magic_link import MagicLinkMethods
from pre_award.common.blueprints import Blueprint
from pre_award.config import Config

api_magic_link_bp = Blueprint("api_magic_links", __name__)


class MagicLinksView(MagicLinkMethods, MethodView):
    @login_requested
    def get(self, link_id: str):
        """
        GET /magic-links/{link_id} endpoint
        If the link_id matches a valid link key, this then:
        - creates a session,
        - sets a session_id cookie in the client
        - sets a session_token cookie in the client
        - deletes the link record from redis
        - deletes the user record from redis
        - then finally, redirects to the redirect_url
        If no matching valid link is found returns a 404 error message
        :param link_id: String short key for the link
        :return: 302 Redirect / 404 Error
        """
        current_app.logger.info(f"[MagicLinksView] L 37")
        fund_short_name = request.args.get("fund")
        round_short_name = request.args.get("round")
        current_app.logger.info(f"[MagicLinksView] L 40")
        fund_data = FundMethods.get_fund(fund_short_name)
        round_data = get_round_data(fund_short_name, round_short_name)
        current_app.logger.info(f"[MagicLinksView] L 43")
        link_key = ":".join([Config.MAGIC_LINK_RECORD_PREFIX, link_id])
        link_hash = self.redis_mlinks.get(link_key)
        if link_hash:
            link = json.loads(link_hash)
            user_key = ":".join(
                [
                    Config.MAGIC_LINK_USER_PREFIX,
                    link.get("accountId"),
                ]
            )
            current_app.logger.info(f"[MagicLinksView] L 54")
            self.redis_mlinks.delete(link_key)
            self.redis_mlinks.delete(user_key)

            # Check account exists
            account = AccountMethods.get_account(account_id=link.get("accountId"))
            current_app.logger.info(f"[MagicLinksView] L 60")
            if not account:
                current_app.logger.error(
                    "Tried to use magic link for non-existent account_id %(account_id)s",
                    dict(account_id=link.get("accountId")),
                )
                redirect(
                    url_for(
                        "magic_links_bp.invalid",
                        fund=fund_short_name,
                        round=round_short_name,
                    )
                )

            # Check link is not expired
            if link.get("exp") > int(datetime.now().timestamp()):
                current_app.logger.info(f"[MagicLinksView] L 76")
                if round_data.has_eligibility:
                    search_params = {
                        "account_id": link.get("accountId"),
                    }
                    has_previous_applicaitons = get_applications_for_account(**search_params)
                    current_app.logger.info(f"[MagicLinksView] L 82")
                    if not has_previous_applicaitons:
                        return AuthSessionBase.create_session_and_redirect(
                            account=account,
                            is_via_magic_link=True,
                            redirect_url=url_for(
                                "eligibility_routes.launch_eligibility",
                                fund_id=fund_data.identifier,
                                round_id=round_data.id,
                            ),
                            fund=fund_short_name,
                            round=round_short_name,
                        )

                return AuthSessionBase.create_session_and_redirect(
                    account=account,
                    is_via_magic_link=True,
                    redirect_url=link.get("redirectUrl"),
                    fund=fund_short_name,
                    round=round_short_name,
                )
            current_app.logger.info(f"[MagicLinksView] L 103")
            return redirect(
                url_for(
                    "magic_links_bp.invalid",
                    error="Link expired",
                    fund=fund_short_name,
                    round=round_short_name,
                )
            )

        elif g.is_authenticated:
            # else if no link exists (or it has been used)
            # but the user is already logged in
            # then redirect them to the global redirect url
            query_params = {
                "fund": fund_short_name,
                "round": round_short_name,
            }
            query_params = {k: v for k, v in query_params.items() if v is not None}
            query_string = urlencode(query_params)
            frontend_account_url = urljoin(Config.APPLICANT_FRONTEND_HOST, f"account?{query_string}")
            current_app.logger.warning(
                "The magic link with hash: '%(link_hash)s' has already been"
                " used but the user with account_id: '%(account_id)s' is"
                " logged in, redirecting to"
                " '%(frontend_account_url)s'.",
                dict(link_hash=link_hash, account_id=g.account_id, frontend_account_url=frontend_account_url),
            )
            current_app.logger.info(f"[MagicLinksView] L 131")
            return redirect(frontend_account_url)
        current_app.logger.info(f"[MagicLinksView] L 133")
        return redirect(
            url_for(
                "magic_links_bp.invalid",
                error="Link expired",
                fund=fund_short_name,
                round=round_short_name,
            )
        )


api_magic_link_bp.add_url_rule("/magic-links/<link_id>", view_func=MagicLinksView.as_view("use"))
