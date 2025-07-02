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


def _derive_status(
    score_map: dict,
    comment_map: dict,
    change_requests: list[AssessmentFlag],
    sub_criteria_id: str,
) -> str:
    has_flag_with_raised_status = False
    has_flag_with_received_status = False
    has_flag_with_accepted_status = False
    for change_request in change_requests:
        if sub_criteria_id in change_request.sections_to_flag:
            if change_request.latest_status.name == FlagType.RAISED.name:
                # Assessor has requested a change — flag is in 'raised' state
                has_flag_with_raised_status = True
                break

            if change_request.latest_status.name == FlagType.RESOLVED.name:
                # Applicant has responded to the change request — flag is 'resolved'
                has_flag_with_received_status = True

            if change_request.latest_status.name == FlagType.STOPPED.name:
                # Assessor has accepted the applicant's response — flag is 'stopped'
                has_flag_with_accepted_status = True

    if has_flag_with_raised_status:
        return Status.CHANGE_REQUESTED.name

    if has_flag_with_received_status:
        return Status.CHANGE_RECEIVED.name

    if has_flag_with_accepted_status or sub_criteria_id in score_map:
        # Either the change request was accepted and scored after applicant responded to it (uncompeted flow)
        # or the sub-criteria has been scored (competed flow)
        return Status.COMPLETED.name

    if sub_criteria_id in comment_map:
        return Status.IN_PROGRESS.name  # if we've commented, but not scored, we're in progress

    # if we haven't commented or scored, we're not started
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
