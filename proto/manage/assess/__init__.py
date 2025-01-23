from flask import render_template

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.services.applications import search_applications
from proto.common.data.services.grants import get_active_round, get_grant

assess_blueprint = Blueprint("assess", __name__)


@assess_blueprint.context_processor
def _grants_service_nav():
    return dict(active_navigation_tab="grants")


@assess_blueprint.get("/grants/<short_code>/applications")
@is_authenticated
def list_grant_applications_handler(short_code):
    active_round, grant = get_active_round(short_code)

    if not active_round:
        grant = get_grant(short_code=short_code)
    applications = search_applications(short_code)
    return render_template("manage/assess/grant_list_applications.jinja.html", applications=applications, grant=grant)
