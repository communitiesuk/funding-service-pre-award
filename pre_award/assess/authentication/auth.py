from flask import g, redirect, request
from fsd_utils.authentication.models import User

from pre_award.assess.authentication.validation import ASSESS_ROLES
from pre_award.assess.services.data_services import get_funds
from pre_award.assess.shared.helpers import get_ttl_hash
from pre_award.config import Config


def auth_protect(unprotected_routes: list):
    """
    Entry gate for the assess blueprint.

    A user is granted access if they hold any role recognised by the assess
    module (see ASSESS_ROLES) on any fund. Fine-grained role requirements for
    specific actions are enforced by the per-route decorators in
    ``pre_award.assess.authentication.validation``; the gate's only job is to
    redirect users with zero assess access away from the blueprint.

    Supports bypassing authorisation via ``DEBUG_USER_ON`` in development.

    Args:
        unprotected_routes: List[str]
            - a list of routes e.g. ["/"] that can be accessed without
              authentication.

    Returns:
        redirect (302) or None if authorised.
    """
    # Every {fund}_{role} string that counts as "has assess access", matching
    # how tokens are emitted at sign-in (upper-cased, fund-prefixed).
    permitted_roles = [
        f"{fund.short_name}_{role}".upper()
        for fund in get_funds(
            get_ttl_hash(seconds=Config.LRU_CACHE_TIME)
        )  # expensive call, so cache it & refresh every 5 minutes
        for role in ASSESS_ROLES
    ]

    if not g.is_authenticated and Config.FLASK_ENV == "development" and Config.DEBUG_USER_ON:
        g.is_authenticated = True
        g.account_id = Config.DEBUG_USER_ACCOUNT_ID
        g.user = User(**Config.DEBUG_USER)
        g.is_debug_user = True
        if request.path in ["/"]:
            return redirect(Config.DASHBOARD_ROUTE)

    elif g.is_authenticated:
        if not g.user.roles or not any(role in g.user.roles for role in permitted_roles):
            return redirect(
                Config.AUTHENTICATOR_HOST + "/service/user" + "?roles_required=" + "|".join(permitted_roles)
            )
        elif request.path in ["", "/"]:
            return redirect(Config.DASHBOARD_ROUTE)
    elif request.path not in unprotected_routes and not request.path.startswith("/static/"):  # noqa
        # Redirect unauthenticated users to login on the home page
        return redirect("/")
