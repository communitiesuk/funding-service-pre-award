from flask import abort, render_template

from data.crud.fund_round_queries import get_fund_and_round
from pre_award.common.blueprints import Blueprint

apply_bp = Blueprint("apply_routes", __name__, template_folder="templates")


@apply_bp.route("/funding-round/<fund_short_name>/<round_short_name>")
def landing_page(fund_short_name: str, round_short_name: str):
    fund, round = get_fund_and_round(fund_short_name, round_short_name)
    if not fund or not round:
        return abort(404)
    return render_template("apply-landing.html", fund=fund, round=round)
