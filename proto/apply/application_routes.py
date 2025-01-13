from flask import render_template

from common.blueprints import Blueprint
from proto.common.data.services.grants import get_grant

application_blueprint = Blueprint("application_blueprint", __name__)


@application_blueprint.get("/grant/<short_code>/apply")
def application_list_handler(short_code):
    # getting the application could also get the round join get the grant - its a specific round once your on the application page
    grant = get_grant(short_code)
    return render_template("application/application_list.jinja.html", grant=grant)
