from flask import render_template

from common.blueprints import Blueprint
from proto.common.data.services.grants import get_active_round, get_grant

grant_blueprint = Blueprint("grant_blueprint", __name__)


@grant_blueprint.get("/grant/<short_code>")
def grant_detail_handler(short_code):
    active_round, grant = get_active_round(short_code)

    if not active_round:
        grant = get_grant(short_code)

    return render_template("grant/grant_detail.jinja.html", grant=grant, active_round=active_round)
