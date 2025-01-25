from flask import redirect, render_template, session, url_for

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.exceptions import DataValidationError, attach_validation_error_to_form
from proto.common.data.models.fund import FundStatus
from proto.common.data.services.grants import create_grant, get_all_grants_with_rounds, get_grant, update_grant
from proto.manage.platform.forms.grants import CreateGrantForm, MakeGrantLiveForm

grants_blueprint = Blueprint("grants", __name__)


@grants_blueprint.context_processor
def _grants_service_nav():
    return dict(active_navigation_tab="grants")


@grants_blueprint.get("/")
@is_authenticated(as_platform_admin=True)
def index():
    grants = get_all_grants_with_rounds()
    return render_template("manage/platform/home.html", grants=grants)


@grants_blueprint.get("/grants/<grant_code>")
@is_authenticated(as_platform_admin=True)
def view_grant_overview(grant_code):
    # it's only ever the top level nav that will use this - all links on the actual page will be relative to
    # the grant you're working on. You'll never randomly jump around because this changes
    session["last_selected_grant_short_code"] = grant_code
    grant = get_grant(grant_code)
    return render_template(
        "manage/platform/view_grant_overview.html",
        grant=grant,
        back_link=url_for("proto_manage.platform.grants.index"),
    )


@grants_blueprint.get("/grants/<grant_code>/application-rounds")
@is_authenticated(as_platform_admin=True)
def view_grant_rounds(grant_code):  # todo: rename everything application-roundy
    grant = get_grant(grant_code)
    return render_template(
        "manage/platform/view_grant_rounds.html",
        grant=grant,
        back_link=url_for("proto_manage.platform.grants.index"),
    )


@grants_blueprint.get("/grants/<grant_code>/reporting-rounds")
@is_authenticated(as_platform_admin=True)
def view_grant_reporting_rounds(grant_code):
    grant = get_grant(grant_code)
    return render_template(
        "manage/platform/view_grant_reporting_rounds.html",
        grant=grant,
        back_link=url_for("proto_manage.platform.grants.index"),
    )


@grants_blueprint.route("/grants/<grant_code>/configuration", methods=("GET", "POST"))
@is_authenticated(as_platform_admin=True)
def view_grant_configuration(grant_code):
    grant = get_grant(grant_code)
    form = MakeGrantLiveForm()
    if form.validate_on_submit():
        update_grant(grant, status=FundStatus.LIVE)
        return redirect(url_for("proto_manage.platform.grants.view_grant_overview", grant_code=grant_code))
    return render_template(
        "manage/platform/view_grant_configuration.html",
        grant=grant,
        form=form,
        back_link=url_for("proto_manage.platform.grants.index"),
    )


@grants_blueprint.route("/create-grant", methods=["GET", "POST"])
@is_authenticated(as_platform_admin=True)
def create_grant_view():
    form = CreateGrantForm()
    if form.validate_on_submit():
        try:
            grant = create_grant(**{k: v for k, v in form.data.items() if k not in {"submit", "csrf_token"}})
        except DataValidationError as e:
            attach_validation_error_to_form(form, e)
        else:
            return redirect(url_for("proto_manage.platform.grants.view_grant_overview", grant_code=grant.short_name))

    return render_template(
        "manage/platform/create_grant.html", form=form, back_link=url_for("proto_manage.platform.grants.index")
    )
