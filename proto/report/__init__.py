from flask import g, render_template

from common.blueprints import Blueprint
from proto.common.auth import is_authenticated
from proto.common.data.services.recipients import get_grant_recipients_for_account

report_blueprint = Blueprint("proto_report", __name__)


@report_blueprint.context_processor
def _grants_service_nav():
    return dict(active_navigation_tab="your_reporting")


@report_blueprint.get("/report")
@report_blueprint.get("/report/")
@is_authenticated
def report_index():
    grant_recipients = get_grant_recipients_for_account(g.account.id)
    return render_template(
        "report/index.html",
        grant_recipients=grant_recipients,
        account=g.account,
    )
