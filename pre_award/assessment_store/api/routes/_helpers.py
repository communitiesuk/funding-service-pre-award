import copy
import json
from uuid import UUID

from flask import current_app, make_response

from pre_award.assess.services.models.flag import FlagType
from pre_award.assessment_store.db.models.assessment_record.enums import Status
from pre_award.assessment_store.db.models.flags.assessment_flag import AssessmentFlag
from pre_award.config import Config


def compress_response(data):
    class UUIDEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, UUID):
                return obj.hex
            return json.JSONEncoder.default(self, obj)

    content = json.dumps(data, cls=UUIDEncoder, separators=(",", ":"))
    response = make_response(content)
    response.headers["Content-length"] = len(content)
    response.headers["Content-Type"] = "application/json"
    return response


def _has_flag_status(change_requests, sub_criteria_id, status_name):
    return any(
        sub_criteria_id in cr.sections_to_flag and cr.latest_status.name == status_name for cr in change_requests
    )


def _derive_status(
    score_map: dict,
    comment_map: dict,
    change_requests: list,
    sub_criteria_id: str,
) -> str:
    if _has_flag_status(change_requests, sub_criteria_id, FlagType.RAISED.name):
        # Assessor has requested a change — flag is in 'raised' state
        return Status.CHANGE_REQUESTED.name

    if _has_flag_status(change_requests, sub_criteria_id, FlagType.RESOLVED.name):
        # Applicant has responded to the change request — flag is 'resolved'
        return Status.CHANGE_RECEIVED.name

    if _has_flag_status(change_requests, sub_criteria_id, FlagType.STOPPED.name) or sub_criteria_id in score_map:
        # Either the change request was accepted and scored after applicant responded to it (uncompeted flow)
        # or the sub-criteria has been scored (competed flow)
        return Status.COMPLETED.name

    if sub_criteria_id in comment_map:
        # If we've commented, but not scored, we're in progress
        return Status.IN_PROGRESS.name

    # If we haven't commented or scored, we're not started
    return Status.NOT_STARTED.name


def transform_to_assessor_task_list_metadata(
    fund_id: str,
    round_id: str,
    score_map: dict,
    comment_map: dict,
    change_requests: list[AssessmentFlag],
) -> tuple[list[dict], list[dict]]:
    current_app.logger.info("Configured fund-rounds:")
    current_app.logger.info(Config.ASSESSMENT_MAPPING_CONFIG.keys())
    mapping = copy.deepcopy(Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"])

    sections = [
        {
            "name": s["name"],
            "sub_criterias": [
                {
                    "name": sc["name"],
                    "id": sc["id"],
                }
                for sc in s["sub_criteria"]
            ],
        }
        for s in mapping["unscored_sections"]
    ]

    criterias = [
        {
            "name": c["name"],
            "total_criteria_score": sum(score_map.get(sc["id"], 0) for sc in c["sub_criteria"]),
            "number_of_scored_sub_criteria": sum(1 for _ in c["sub_criteria"]),
            "weighting": c["weighting"],
            "sub_criterias": [
                {
                    "name": sc["name"],
                    "id": sc["id"],
                    "score": score_map.get(sc["id"]),
                    "theme_count": len(sc["themes"]),
                    "status": _derive_status(score_map, comment_map, change_requests, sc["id"]),
                }
                for sc in c["sub_criteria"]
            ],
        }
        for c in mapping["scored_criteria"]
    ]

    return sections, criterias
