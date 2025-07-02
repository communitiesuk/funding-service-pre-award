from distutils.util import strtobool
from typing import Dict, List

from flask import request

from pre_award.assess.services.data_services import is_uncompeted_flow
from pre_award.assessment_store.db.queries import (
    create_score_for_app_sub_crit,
    get_scores_for_app_sub_crit,
    get_scoring_system_for_round_id,
)
from pre_award.assessment_store.db.queries.assessment_records.queries import find_assessor_task_list_state
from pre_award.assessment_store.db.queries.scores.queries import accept_sub_criteria
from pre_award.common.blueprints import Blueprint

assessment_score_bp = Blueprint("assessment_score_bp", __name__)


@assessment_score_bp.get("/scoring-system/<round_id>")
def get_scoring_system_name_for_round_id(round_id: str) -> dict:
    """get_scoring_system_for_round_id Function used by the get endpoint
    `/scoring_systems/{round_id}`.

    :param round_id: The stringified round UUID.
    :return: A dictionary.

    """

    scoring_system = get_scoring_system_for_round_id(round_id)
    return {
        "round_id": round_id,
        "scoring_system": scoring_system["scoring_system_name"].name,
    }


@assessment_score_bp.get("/score")
def get_score_for_application_sub_criteria() -> List[Dict]:
    """get_score_for_application_sub_criteria Function used by the get endpoint
    `/applications/{application_id}/ subcriterias/{subcriteria_id}/scores`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param score_history: Boolean to return all scores if true
    :return: A List of dictionaries.

    """
    application_id = request.args.get("application_id")
    sub_criteria_id = request.args.get("sub_criteria_id")
    score_history = (
        bool(strtobool(request.args.get("score_history", "false"))) if "score_history" in request.args else None
    )

    score_metadata = get_scores_for_app_sub_crit(application_id, sub_criteria_id, score_history)

    return score_metadata


@assessment_score_bp.post("/score")
def post_score_for_application_sub_criteria() -> Dict:
    """post_score_for_application_sub_criteria Function used by the post endpoint
    `/applications/{application_id}/ subcriterias/{subcriteria_id}/scores`.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :return: A dictionary.

    """
    args = request.get_json()
    application_id = args["application_id"]
    sub_criteria_id = args["sub_criteria_id"]
    score = args["score"]
    justification = args["justification"]
    user_id = args["user_id"]

    tasklist_metadata = find_assessor_task_list_state(application_id)

    if is_uncompeted_flow(tasklist_metadata["fund_id"]):
        created_score = accept_sub_criteria(
            application_id=application_id,
            sub_criteria_id=sub_criteria_id,
            user_id=user_id,
            message=justification,
            score=score,
        )
    else:
        created_score = create_score_for_app_sub_crit(
            application_id=application_id,
            sub_criteria_id=sub_criteria_id,
            score=score,
            justification=justification,
            user_id=user_id,
        )

    return created_score
