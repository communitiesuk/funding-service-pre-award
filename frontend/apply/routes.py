from flask import abort, render_template

from pre_award.common.blueprints import Blueprint
from services.data.queries.fund_round_queries import get_fund_and_round

apply_bp = Blueprint("apply_routes", __name__, template_folder="templates")


@apply_bp.route("/monolith/<fund_short_name>/<round_short_name>")
def landing_page(fund_short_name: str, round_short_name: str):
    fund, round = get_fund_and_round(fund_short_name, round_short_name)
    if not fund or not round:
        return abort(404)
    return render_template("apply/apply-landing.html.jinja", fund=fund, round=round)
