from flask import redirect, render_template, session, url_for

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.services.applications import search_applications
from proto.common.data.services.grants import get_active_round, get_all_grants_with_rounds, get_grant

assess_blueprint = Blueprint("assess", __name__)


@assess_blueprint.context_processor
def _grants_service_nav():
    return dict(active_navigation_tab="applications")


@assess_blueprint.get("/route/grants/applications")
@is_authenticated(as_platform_admin=True)
def route_grant_applications():
    if session.get("last_selected_grant_short_code"):
        return redirect(
            url_for(
                "proto_manage.assess.list_grant_applications_handler",
                short_code=session.get("last_selected_grant_short_code"),
            )
        )
    else:
        grants = get_all_grants_with_rounds()
        selected_grant = grants[0]
        if selected_grant:
            return redirect(
                url_for("proto_manage.assess.list_grant_applications_handler", short_code=selected_grant.short_name)
            )
        else:
            return redirect(url_for("proto_manage.platform.grants.index"))


@assess_blueprint.get("/grants/<short_code>/applications")
@is_authenticated(as_platform_admin=True)
def list_grant_applications_handler(short_code):
    active_round, grant = get_active_round(short_code)

    if not active_round:
        grant = get_grant(short_code=short_code)
    applications = search_applications(short_code)
    return render_template("manage/assess/grant_list_applications.jinja.html", applications=applications, grant=grant)
