from flask import g, redirect, render_template, url_for

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.services.accounts import get_account
from proto.common.data.services.applications import (
    create_application,
    get_application,
    get_application_grants,
    get_applications,
)
from proto.common.data.services.grants import get_active_round, get_grant

application_blueprint = Blueprint("application", __name__)


@application_blueprint.get("/grant/<short_code>/apply")
@is_authenticated
def application_list_handler(short_code):
    account = {"email": g.account.email}  # this should be uniformly serialised from the db or the session somewhere

    applications = get_applications(account_id=g.account.id)

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


@application_blueprint.post("/grant/<short_code>/apply")
@is_authenticated
def application_new_handler(short_code):
    account = get_account(g.account.id)

    active_round, grant = get_active_round(short_code)

    if not active_round:
        raise Exception("Cannot start an application with no active application round")

    application = create_application(preview=False, round_id=active_round.id, account_id=account.id)
    return redirect(url_for("proto_apply.application.application_tasklist", application_id=application.id))


@application_blueprint.get("/applications")
@is_authenticated
def all_user_application_list_handler():
    account = get_account(g.account.id)
    grants = get_application_grants(g.account.id)
    return render_template(
        "apply/application/all_applications_grant_list.jinja.html",
        grants=grants,
        account=account,
        active_navigation_tab="your_grants",
    )


@application_blueprint.get("/application/<application_id>")
@is_authenticated
def application_tasklist(application_id):
    account = get_account(g.account.id)
    application = get_application(application_id)
    return render_template("form_runner/application_tasklist.html", application=application, account=account)
