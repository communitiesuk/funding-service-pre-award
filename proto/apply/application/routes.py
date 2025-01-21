from flask import render_template, session

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.services.applications import get_applications
from proto.common.data.services.grants import get_active_round, get_grant

application_blueprint = Blueprint("application", __name__)


@application_blueprint.get("/grant/<short_code>/apply")
@is_authenticated
def application_list_handler(short_code):
    account = {
        "email": session.get("magic_links_account_email")
    }  # this should be uniformly serialised from the db or the session somewhere

    applications = get_applications(account_id=session.get("magic_links_account_id"))

    active_round, grant = get_active_round(short_code)

    if not active_round:
        grant = get_grant(short_code)

    return render_template(
        "apply/application/application_list.jinja.html",
        grant=grant,
        active_round=active_round,
        applications=applications,
        account=account,
    )
