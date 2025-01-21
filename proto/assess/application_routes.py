from flask import render_template

from common.blueprints import Blueprint
from proto.common.data.services.applications import search_applications
from proto.common.data.services.grants import get_active_round, get_grant

# we'll probably have the steer to put this in with the admin/ management tool
# permissions would then separate your ability to set things up and just do assessments
# the core assesssments workflow should be really similar, with no ability to self serve new grants or see too many details
# (that will the be the hardest part I think)
assessment_blueprint = Blueprint("assessment_blueprint", __name__)


@assessment_blueprint.get("/grant/<short_code>/applications")
def list_applications_for_assessment_handler(short_code):
    active_round, grant = get_active_round(short_code)

    if not active_round:
        grant = get_grant(short_code=short_code)
    applications = search_applications(short_code)
    return render_template("grant_list_applications.jinja.html", applications=applications, grant=grant)
