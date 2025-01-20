from flask import render_template, session

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.services.applications import get_applications
from proto.common.data.services.grants import get_active_round, get_grant

application_blueprint = Blueprint("application_blueprint", __name__)


@application_blueprint.get("/grant/<short_code>/apply")
@is_authenticated
def application_list_handler(short_code):
    # I'm storing the email in the session so don't actually need to look this up int he database, it definitely could and should though
    # this being available to the view is probably a candidate for authenticated context processors that happen before the handler in the middleware
    # account = get_account(session.get("magic_links_account_id"))
    account = {"email": session.get("magic_links_account_email")}

    # ideally this would be application join rounds (which might even subsequently join fund?)
    # if we want to individually fetch that separately anyway thats fine
    applications = get_applications(account_id=session.get("magic_links_account_id"))

    # getting the application could also get the round join get the grant - its a specific round once your on the application page
    active_round, grant = get_active_round(short_code)

    if not active_round:
        grant = get_grant(short_code)
    # grant = get_grant(short_code)
    return render_template(
        "application/application_list.jinja.html",
        grant=grant,
        active_round=active_round,
        applications=applications,
        account=account,
    )
