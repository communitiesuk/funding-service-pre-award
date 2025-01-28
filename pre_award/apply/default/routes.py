from flask import abort, current_app, redirect, render_template

from pre_award.apply.default.data import get_default_round_for_fund, get_ttl_hash
from pre_award.apply.helpers import get_all_fund_short_names
from pre_award.common.blueprints import Blueprint
from pre_award.config import Config

default_bp = Blueprint("routes", __name__, template_folder="templates")


@default_bp.route("/")
def index():
    return abort(404)


@default_bp.route("/funding-round/<fund_short_name>")
def index_fund_only(fund_short_name):
    if str.upper(fund_short_name) in get_all_fund_short_names(get_ttl_hash(Config.LRU_CACHE_TIME)):
        current_app.logger.info(
            "In fund-only start page route for %(fund_short_name)s", dict(fund_short_name=fund_short_name)
        )
        default_round = get_default_round_for_fund(fund_short_name=fund_short_name)
        if default_round:
            return redirect(f"/funding-round/{fund_short_name}/{default_round.short_name}")

        current_app.logger.warning(
            "Unable to retrieve default round for fund %(fund_short_name)s", dict(fund_short_name=fund_short_name)
        )
    return (
        render_template(
            "apply/404.html",
            round_data={},
        ),
        404,
    )
