from flask import g, render_template, request, url_for
from fsd_utils.authentication.decorators import login_requested

from pre_award.common.blueprints import Blueprint
from pre_award.config import Config

user_bp = Blueprint(
    "user_bp",
    __name__,
    url_prefix="/service/user",
    template_folder="templates",
)


@user_bp.route("")
@login_requested
def user():
    """
    Route to display user status, renders user.html
    with roles_required, logged_in_user and login/
    logout urls.
    Query Args:
       - roles_required: List[str] is set by checking if logged_in_user has all roles required
       - source_app: SupportedApp is set by the app that is requesting the user page
    """
    status_code = 200
    roles_required = request.args.get("roles_required")
    source_app = request.args.get("source_app")
    logged_in_user = g.user if g.is_authenticated else None
    if logged_in_user:
        if roles_required:
            if logged_in_user.roles and all(
                role_required in logged_in_user.roles for role_required in roles_required.upper().split("|")
            ):
                roles_required = None
            else:
                status_code = 403
    return (
        render_template(
            "authenticator/user/user.html",
            roles_required=roles_required,
            logged_in_user=logged_in_user,
            login_url=url_for("api_sso.login"),
            logout_url=url_for("api_sso.logout"),
            support_desk_assess=Config.SUPPORT_DESK_ASSESS,
            source_app=source_app,
        ),
        status_code,
    )
