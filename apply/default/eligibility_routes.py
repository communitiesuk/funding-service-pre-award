from flask import current_app, redirect, render_template, request, url_for
from fsd_utils.authentication.decorators import login_required

from apply.helpers import format_rehydrate_payload, get_fund_and_round, get_token_to_return_to_application
from common.blueprints import Blueprint
from config import Config

eligibility_bp = Blueprint("eligibility_routes", __name__, template_folder="templates")


@eligibility_bp.route("/eligibility-result/<fund_short_name>/<round_name>", methods=["GET"])
@login_required
def eligiblity_result(fund_short_name, round_name):
    """Render the eligibility result page"""
    redirect_to_eligible_round = request.args.get("redirect_to_eligible_round")

    # change round name if redirect_to_eligible_round is set in coming request from form runner
    if redirect_to_eligible_round:
        round_name = redirect_to_eligible_round

    current_app.logger.info(
        "Eligibility launch result: {fund_short_name} {round_name}",
        extra=dict(fund_short_name=fund_short_name, round_name=round_name),
    )
    return_url = request.host_url + url_for("account_routes.dashboard", fund=fund_short_name, round=round_name)
    fund, round = get_fund_and_round(fund_short_name=fund_short_name, round_short_name=round_name)
    current_app.logger.info("Eligibility return url: {return_url}", extra=dict(return_url=return_url))
    return render_template(
        "apply/eligibility_result.html",
        fund_id=round.fund_id,
        round_id=round.id,
        fund_title=fund.title,
        backLink=return_url,
    )


@eligibility_bp.route("/launch-eligibility/<fund_id>/<round_id>", methods=["POST"])
@login_required
def launch_eligibility(fund_id, round_id):
    """Launch eligibility page/form"""
    fund_details, round_details = get_fund_and_round(fund_id=fund_id, round_id=round_id)
    fund_name = fund_details.short_name.lower()
    round_name = round_details.short_name.lower()
    form_name = f"{fund_name}-{round_name}-eligibility"

    current_app.logger.info(
        "Eligibility launch request for fund {fund_name} round {round_name}",
        extra=dict(fund_name=fund_name, round_name=round_name),
    )

    return_url = request.host_url + url_for("account_routes.dashboard", fund=fund_name, round=round_name)

    current_app.logger.info("Url the form runner should return to '{return_url}'.", extra=dict(return_url=return_url))

    rehydrate_payload = format_rehydrate_payload(
        form_data={"questions": []},
        application_id=None,
        returnUrl=return_url,
        form_name=form_name,
        markAsCompleteEnabled=False,  # assume we don't have it for eligibility
        fund_name=fund_name,
        round_name=round_name,
        has_eligibility=round_details.has_eligibility,
    )
    rehydration_token = get_token_to_return_to_application(form_name, rehydrate_payload)

    redirect_url = Config.FORM_REHYDRATION_URL.format(rehydration_token=rehydration_token)
    if Config.FORMS_SERVICE_PRIVATE_HOST:
        redirect_url = redirect_url.replace(Config.FORMS_SERVICE_PRIVATE_HOST, Config.FORMS_SERVICE_PUBLIC_HOST)
    return redirect(redirect_url)