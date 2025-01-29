from flask import abort, render_template, request

from data.crud.fund_round_queries import get_fund, get_round
from pre_award.common.blueprints import Blueprint

apply_bp = Blueprint("apply_routes", __name__, template_folder="templates")


@apply_bp.route("/funding-round/<fund_short_name>/<round_short_name>")
def landing_page(fund_short_name: str, round_short_name: str) -> str:
    round = get_round(fund_short_name, round_short_name)
    if not round:
        return abort(404)
    return render_template("apply/landing.html", fund=round.fund, round=round)


@apply_bp.route("/contact_us", methods=["GET"])
def contact_us() -> str:
    fund_short_name = request.args.get("fund_short_name", None)
    fund = get_fund(fund_short_name=fund_short_name) if fund_short_name else None
    return render_template("apply/contact-us.html", fund=fund)
