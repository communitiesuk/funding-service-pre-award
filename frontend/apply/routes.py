from flask import render_template

from pre_award.common.blueprints import Blueprint
from services.data.queries.fund_round_queries import get_fund_and_round

apply_bp = Blueprint("apply_routes", __name__, template_folder="templates")


@apply_bp.route("/monolith/<fund_short_name>/<round_short_name>")
def landing_page(fund_short_name: str, round_short_name: str):
    fund, round = get_fund_and_round(fund_short_name, round_short_name)
    return render_template("apply/landing-mono.html", fund=fund, round=round)
