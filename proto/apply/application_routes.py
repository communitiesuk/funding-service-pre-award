from flask import render_template

from common.blueprints import Blueprint
from proto.common.data.services.applications import get_applications
from proto.common.data.services.grants import get_active_round, get_grant

application_blueprint = Blueprint("application_blueprint", __name__)


@application_blueprint.get("/grant/<short_code>/apply")
def application_list_handler(short_code):
    # ideally this would be application join rounds (which might even subsequently join fund?)
    # if we want to individually fetch that separately anyway thats fine
    applications = get_applications()

    # getting the application could also get the round join get the grant - its a specific round once your on the application page
    active_round, grant = get_active_round(short_code)

    if not active_round:
        grant = get_grant(short_code)
    # grant = get_grant(short_code)
    return render_template(
        "application/application_list.jinja.html", grant=grant, active_round=active_round, applications=applications
    )
