from flask import g, render_template

from common.blueprints import Blueprint
from proto.common.auth import maybe_authenticated
from proto.common.data.services.grants import get_active_round, get_grant
from proto.common.data.services.round import get_open_rounds

grant_blueprint = Blueprint("grant_blueprint", __name__)


@grant_blueprint.get("/grant")
@grant_blueprint.get("/grant/")
@maybe_authenticated
def all_open_grants_handler():
    rounds = get_open_rounds()
    return render_template("apply/grant/all_grants.jinja.html", rounds=rounds)


@grant_blueprint.get("/grant/<short_code>")
@maybe_authenticated
def grant_detail_handler(short_code):
    active_round, grant = get_active_round(short_code)

    if not active_round:
        grant = get_grant(short_code)

    return render_template(
        "apply/grant/grant_detail.jinja.html", grant=grant, active_round=active_round, account=g.account
    )
