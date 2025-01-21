import copy
from typing import List

from flask import request

from pre_award.assessment_store.db.queries.progress.queries import get_progress_for_app
from pre_award.common.blueprints import Blueprint
from pre_award.config import Config

assessment_progress_bp = Blueprint("assessment_progress_bp", __name__)


@assessment_progress_bp.post("/progress/<fund_id>/<round_id>")
def post_progress_for_applications(fund_id, round_id) -> List[dict]:
    application_ids = request.get_json()["application_ids"]
    return get_progress_for_applications(fund_id, round_id, application_ids=application_ids)


@assessment_progress_bp.get("/progress/<fund_id>/<round_id>")
def get_progress_for_applications(fund_id, round_id, application_ids=None) -> List[dict]:
    application_ids = request.args.getlist("application_ids") if application_ids is None else application_ids
    scored_criteria = copy.deepcopy(Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"])["scored_criteria"]
    scored_sub_crit_list = [
        subcrit["id"] for crit in scored_criteria for subcrit in crit["sub_criteria"] if subcrit["id"] != "themes"
    ]
    app_prog_list = get_progress_for_app(application_ids)
    for app in app_prog_list:
        app["progress"] = int(100 * app["scored_sub_criterias"] / len(scored_sub_crit_list))

    return app_prog_list
