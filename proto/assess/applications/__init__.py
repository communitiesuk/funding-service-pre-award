from flask import render_template

from common.blueprints import Blueprint
from proto.common.data.services.applications import search_applications
from proto.common.data.services.grants import get_active_round, get_grant

applications_blueprint = Blueprint("assess_application_blueprint", __name__)


@applications_blueprint.get("/grant/<short_code>/applications")
def list_applications_for_assessment_handler(short_code):
    active_round, grant = get_active_round(short_code)

    if not active_round:
        grant = get_grant(short_code=short_code)
    applications = search_applications(short_code)
    return render_template(
        "assess/applications/grant_list_applications.jinja.html", applications=applications, grant=grant
    )
