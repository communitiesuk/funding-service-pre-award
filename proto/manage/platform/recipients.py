from flask import redirect, render_template, session, url_for

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.services.applications import get_application, search_applications
from proto.common.data.services.grants import get_all_grants_with_rounds, get_grant
from proto.common.data.services.recipients import (
    create_recipient_from_application,
    get_grant_recipient,
    search_recipients,
    update_grant_recipient,
)
from proto.manage.platform.forms.recipients import (
    SetupNewRecipientFlowForm,
    SetupNewRecipientFromApplicationForm,
    UpdateRecipientFundingAllocationForm,
)

recipients_blueprint = Blueprint("recipients", __name__)


@recipients_blueprint.context_processor
def _recipients_service_nav():
    return dict(active_navigation_tab="recipients")


@recipients_blueprint.get("/recipients")
@recipients_blueprint.get("/recipients/")
@is_authenticated(as_platform_admin=True)
def index():
    if session.get("last_selected_grant_short_code"):
        return redirect(
            url_for(
                "proto_manage.platform.recipients.list_grant_recipients",
                short_code=session.get("last_selected_grant_short_code"),
            )
        )
    else:
        grants = get_all_grants_with_rounds()
        selected_grant = grants[0]
        if selected_grant:
            return redirect(
                url_for("proto_manage.platform.recipients.list_grant_recipients", short_code=selected_grant.short_name)
            )
        else:
            return redirect(url_for("proto_manage.platform.grants.index"))


@recipients_blueprint.get("/recipients/<short_code>")
@is_authenticated(as_platform_admin=True)
def list_grant_recipients(short_code):
    grant = get_grant(short_code)
    recipients = search_recipients(short_code)
    return render_template("manage/platform/recipients/index.html", recipients=recipients, grant=grant)


@recipients_blueprint.route("/recipients/<short_code>/setup-recipient", methods=["GET", "POST"])
@is_authenticated(as_platform_admin=True)
def choose_new_recipient_flow(short_code):
    grant = get_grant(short_code)
    form = SetupNewRecipientFlowForm()
    if form.validate_on_submit():
        if form.flow.data == "application":
            return redirect(
                url_for(
                    "proto_manage.platform.recipients.choose_application_for_new_grant_recipient", short_code=short_code
                )
            )
    return render_template("manage/platform/recipients/choose-new-recipient-flow.html", grant=grant, form=form)


@recipients_blueprint.route("/recipients/<short_code>/setup-recipient/select-application", methods=["GET", "POST"])
@is_authenticated(as_platform_admin=True)
def choose_application_for_new_grant_recipient(short_code):
    grant = get_grant(short_code)
    form = SetupNewRecipientFromApplicationForm(applications=search_applications(short_code))
    if form.validate_on_submit():
        application = get_application(form.application.data)
        recipient = create_recipient_from_application(application)
        return redirect(
            url_for(
                "proto_manage.platform.recipients.view_grant_recipient",
                short_code=short_code,
                recipient_id=recipient.id,
            )
        )
    return render_template(
        "manage/platform/recipients/choose-application-for-new-grant-recipient.html", grant=grant, form=form
    )


@recipients_blueprint.route("/recipients/<short_code>/<uuid:recipient_id>", methods=["GET", "POST"])
@is_authenticated(as_platform_admin=True)
def view_grant_recipient(short_code, recipient_id):
    recipient = get_grant_recipient(short_code, recipient_id)
    return render_template(
        "manage/platform/recipients/view-grant-recipient.html",
        recipient=recipient,
        grant=recipient.application.round.proto_grant,
    )


@recipients_blueprint.route(
    "/recipients/<short_code>/<uuid:recipient_id>/update-funding-allocation", methods=["GET", "POST"]
)
@is_authenticated(as_platform_admin=True)
def update_grant_recipient_funding_allocation(short_code, recipient_id):
    recipient = get_grant_recipient(short_code, recipient_id)
    form = UpdateRecipientFundingAllocationForm(obj=recipient)
    if form.validate_on_submit():
        update_grant_recipient(recipient, funding_allocated=form.funding_allocated.data)
        return redirect(
            url_for(
                "proto_manage.platform.recipients.view_grant_recipient",
                short_code=short_code,
                recipient_id=recipient_id,
            )
        )
    return render_template(
        "manage/platform/recipients/update-funding-allocation.html",
        recipient=recipient,
        form=form,
        grant=recipient.application.round.proto_grant,
    )
