from flask import abort, current_app, render_template

from data.crud.fund_round_queries import get_fund_and_round
from pre_award.common.blueprints import Blueprint

apply_bp = Blueprint("apply_routes", __name__, template_folder="templates")


@apply_bp.route("/funding-round/<fund_short_name>/<round_short_name>")
def landing_page(fund_short_name: str, round_short_name: str):
    current_app.logger.info(
        "Apply landing page for fund %(fund_short_name)s, round %(round_short_name)s",
        dict(fund_short_name=fund_short_name, round_short_name=round_short_name),
    )
    fund, round = get_fund_and_round(fund_short_name, round_short_name)
    if not fund or not round:
        return abort(404)
    return render_template("apply/landing.html", fund=fund, round=round)
