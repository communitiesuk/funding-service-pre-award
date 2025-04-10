import copy
from decimal import ROUND_HALF_UP, Decimal
from typing import Dict, List

from flask import Response, current_app, request

from pre_award.assessment_store.api.models.sub_criteria import SubCriteria
from pre_award.assessment_store.api.routes._helpers import compress_response, transform_to_assessor_task_list_metadata
from pre_award.assessment_store.api.routes.subcriterias.get_sub_criteria import (
    get_all_subcriteria,
    return_subcriteria_from_mapping,
)
from pre_award.assessment_store.config.mappings.assessment_mapping_fund_round import (
    applicant_info_mapping,
)
from pre_award.assessment_store.db.models.flags.flag_update import FlagStatus
from pre_award.assessment_store.db.queries import get_metadata_for_fund_round_id
from pre_award.assessment_store.db.queries.assessment_records.queries import (
    find_assessor_task_list_state,
    get_application_jsonb_blob,
    get_assessment_export_data,
    get_assessment_sub_critera_state,
    get_metadata_for_application,
    update_status_to_completed,
)
from pre_award.assessment_store.db.queries.comments.queries import get_sub_criteria_to_has_comment_map
from pre_award.assessment_store.db.queries.flags.queries import get_flags_for_application
from pre_award.assessment_store.db.queries.qa_complete.queries import (
    get_qa_complete_record_for_application,
)
from pre_award.assessment_store.db.queries.scores.queries import (
    get_scoring_system_for_round_id,
    get_sub_criteria_to_latest_score_map,
)
from pre_award.common.blueprints import Blueprint
from pre_award.config import Config

assessment_assessment_bp = Blueprint("assessment_assessment_bp", __name__)


def calculate_overall_score_percentage_for_application(application_id, fund_id, round_id):
    scoring_system = get_scoring_system_for_round_id(round_id)

    # Deep copy the assessment mapping configuration for the specific fund and round
    mapping = copy.deepcopy(Config.ASSESSMENT_MAPPING_CONFIG[f"{fund_id}:{round_id}"])
    sub_criteria_to_criteria_weighting_map = {}
    highest_possible_weighted_score_for_round = 0
    if mapping["scored_criteria"] == []:
        # We have no scoring config for this round (possibly an EOI)
        current_app.logger.info(
            "No scoring config found for %(fund_id)s:%(round_id)s",
            dict(fund_id=fund_id, round_id=round_id),
        )
        return None

    # Combine mapping and highest possible score calculation
    for criterion in mapping["scored_criteria"]:
        parent_weighting = criterion["weighting"]
        if "sub_criteria" in criterion:
            num_sub_criteria = len(criterion["sub_criteria"])
            for sub_criterion in criterion["sub_criteria"]:
                sub_criteria_to_criteria_weighting_map[sub_criterion["id"]] = parent_weighting
            # Update the highest possible weighted score
            highest_possible_weighted_score_for_round += (
                scoring_system["maximum_score"] * parent_weighting * num_sub_criteria
            )

    application_weighted_score = sum(
        sub_criteria_score * sub_criteria_to_criteria_weighting_map[sub_criteria]
        for sub_criteria, sub_criteria_score in get_sub_criteria_to_latest_score_map(application_id).items()
    )
    score = (application_weighted_score / highest_possible_weighted_score_for_round) * 100
    rounded_score = Decimal(score).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(rounded_score)


@assessment_assessment_bp.get("/application/<application_id>/metadata")
def assessment_metadata_for_application_id(application_id: str) -> Dict:
    return get_metadata_for_application(application_id)


def _fix_country(country):
    country = country.strip().casefold()
    if country == "northernireland":
        country = "northern ireland"
    return country


@assessment_assessment_bp.get("/application_overviews/<fund_id>/<round_id>")
def all_assessments_for_fund_round_id(
    fund_id: str,
    round_id: str,
) -> List[Dict]:
    """all_assessments_for_fund_round_id Function used by the endpoint
    `/application_overviews/{fund_id}/{round_id}`.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A list of dictionaries.

    """
    search_term: str = request.args.get("search_term", "")
    funding_type: str = request.args.get("funding_type", "ALL")
    asset_type: str = request.args.get("asset_type", "ALL")
    status: str = request.args.get("status", "ALL")
    search_in: str = request.args.get("search_in", "")
    countries: str = request.args.get("countries", "all")
    filter_by_tag: str = request.args.get("filter_by_tag", "")
    country: str = request.args.get("country", "ALL")
    region: str = request.args.get("region", "ALL")
    local_authority: str = request.args.get("local_authority", "ALL")
    cohort: str = request.args.get("cohort", "ALL")
    publish_datasets: str = request.args.get("publish_datasets", "ALL")
    datasets: str = request.args.get("datasets", "ALL")
    team_in_place: str = request.args.get("team_in_place", "ALL")
    joint_application: str = request.args.get("joint_application", "ALL")

    app_list = get_metadata_for_fund_round_id(
        fund_id=fund_id,
        round_id=round_id,
        search_term=search_term,
        asset_type=asset_type,
        status=status,
        countries=[_fix_country(c) for c in countries.split(",") if c],
        search_in=search_in,
        funding_type=funding_type,
        filter_by_tag=filter_by_tag,
        country=country,
        region=region,
        local_authority=local_authority,
        cohort=cohort,
        publish_datasets=publish_datasets,
        datasets=datasets,
        team_in_place=team_in_place,
        joint_application=joint_application,
    )

    # Calculate and assign score percentages for each application
    for app in app_list:
        app["overall_score_percentage"] = calculate_overall_score_percentage_for_application(
            application_id=app["application_id"], fund_id=app["fund_id"], round_id=app["round_id"]
        )

    return compress_response(app_list)


@assessment_assessment_bp.get("/sub_criteria_overview/<application_id>/<sub_criteria_id>")
def sub_criteria(application_id, sub_criteria_id) -> Dict:
    """Returns metadata and themes for a sub_criteria
    `/sub_criteria_overview/{sub_criteria_id}`.

    :param sub_criteria_id: The stringified sub criteria id (NOT sub
        critria name).
    :return: A sub criteria dictionary.

    """
    current_app.logger.info(
        "Processing request for sub criteria: %(sub_criteria_id)s.", dict(sub_criteria_id=sub_criteria_id)
    )
    metadata = find_assessor_task_list_state(application_id)
    current_app.logger.info(
        "Searching assessment mapping for sub criteria: %(sub_criteria_id)s.", dict(sub_criteria_id=sub_criteria_id)
    )
    sub_criteria_config_from_mapping = return_subcriteria_from_mapping(
        sub_criteria_id,
        metadata["fund_id"],
        metadata["round_id"],
        metadata["language"],
    )
    current_app.logger.info(
        "Getting application subcriteria metadata for application: %(sub_criteria_id)s.",
        dict(sub_criteria_id=sub_criteria_id),
    )
    application_metadata_for_subcriteria = get_assessment_sub_critera_state(application_id)
    sub_criteria = SubCriteria.from_filtered_dict(
        {
            **sub_criteria_config_from_mapping,
            **application_metadata_for_subcriteria,
        }
    )
    sub_criteria_dict = sub_criteria.to_dict()
    return sub_criteria_dict


@assessment_assessment_bp.get("/sub_criteria_overview/banner_state/<application_id>")
def get_banner_state(application_id: str) -> dict:
    return get_assessment_sub_critera_state(application_id)


@assessment_assessment_bp.get("/application_overviews/<application_id>")
def get_assessor_task_list_state(application_id: str) -> dict:
    """get_assessor_task_list_state Function used by the endpoint
    `/assessor_task_list/{application_id}`.

    :param application_id: The stringified application UUID.
    :return: A dictionary.

    """

    metadata = find_assessor_task_list_state(application_id)
    score_map = get_sub_criteria_to_latest_score_map(application_id)
    comment_map = get_sub_criteria_to_has_comment_map(application_id)
    change_requests = [flag for flag in get_flags_for_application(application_id) if flag.is_change_request]
    sections, criterias = transform_to_assessor_task_list_metadata(
        metadata["fund_id"], metadata["round_id"], score_map, comment_map, change_requests
    )
    qa_complete = get_qa_complete_record_for_application(application_id)

    metadata["sections"] = sections
    metadata["criterias"] = criterias
    metadata["qa_complete"] = qa_complete

    return metadata


@assessment_assessment_bp.get("/sub_criteria_themes/<application_id>")
def get_application_json_and_sub_criterias(application_id: str):
    metadata = find_assessor_task_list_state(application_id)
    return {
        "application_json": get_application_jsonb_blob(application_id),
        "sub_criterias": get_all_subcriteria(
            metadata["fund_id"],
            metadata["round_id"],
            metadata["language"],
        ),
    }


@assessment_assessment_bp.post("/application/<application_id>/status/complete")
def update_ar_status_to_completed(application_id: str):
    """Function updates the status to COMPLETE for the given application_id."""
    update_status_to_completed(application_id)

    return Response(
        status=204,
    )


@assessment_assessment_bp.post("/assessments/get-stats/<fund_id>")
def assessment_stats_for_multiple_round_ids(
    fund_id: str,
):
    round_ids = request.get_json().get("round_ids") or []
    return {
        round_id: assessment_stats_for_fund_round_id(
            fund_id,
            round_id,
        )
        for round_id in round_ids
    }


@assessment_assessment_bp.get("/assessments/get-stats/<fund_id>/<round_id>")
def assessment_stats_for_fund_round_id(
    fund_id: str,
    round_id: str,
) -> List[Dict]:
    """Function used by the endpoint `/assessments/get-stats/{fund_id}/{round_id}`
    that returns a dictionary of metrics about assessments for a given fund_id and
    round_id.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A list of dictionaries.

    """
    search_term: str = request.args.get("search_term", "")
    asset_type: str = request.args.get("asset_type", "ALL")
    status: str = request.args.get("status", "ALL")
    search_in: str = request.args.get("search_in", "")
    funding_type: str = request.args.get("funding_type", "ALL")
    countries: str = request.args.get("countries", "all")

    def determine_display_status(assessment):
        all_latest_status = [flag["latest_status"] for flag in assessment["flags"]]
        if FlagStatus.STOPPED in all_latest_status:
            display_status = "STOPPED"
        elif all_latest_status.count(FlagStatus.RAISED) > 1:
            display_status = "MULTIPLE_FLAGS"
        elif all_latest_status.count(FlagStatus.RAISED) == 1:
            display_status = "FLAGGED"
        elif assessment["is_qa_complete"]:
            display_status = "QA_COMPLETED"
        else:
            display_status = assessment["workflow_status"]
        return display_status

    stats = {}
    assessments = get_metadata_for_fund_round_id(
        fund_id=fund_id,
        round_id=round_id,
        search_term=search_term,
        asset_type=asset_type,
        status=status,
        search_in=search_in,
        funding_type=funding_type,
        countries=[_fix_country(c) for c in countries.split(",") if c],
    )
    stats.update(
        {
            "completed": len([1 for assessment in assessments if determine_display_status(assessment) == "COMPLETED"]),
            "assessing": len(
                [1 for assessment in assessments if determine_display_status(assessment) == "IN_PROGRESS"]
            ),
            "not_started": len(
                [1 for assessment in assessments if determine_display_status(assessment) == "NOT_STARTED"]
            ),
            "qa_completed": len(
                [1 for assessment in assessments if determine_display_status(assessment) == "QA_COMPLETED"]
            ),
            "stopped": len([1 for assessment in assessments if determine_display_status(assessment) == "STOPPED"]),
            "flagged": len([1 for assessment in assessments if determine_display_status(assessment) == "FLAGGED"]),
            "multiple_flagged": len(
                [1 for assessment in assessments if determine_display_status(assessment) == "MULTIPLE_FLAGS"]
            ),
            "total": len(assessments),
        }
    )

    return stats


@assessment_assessment_bp.get("/application/<application_id>/json")
def get_application_json(application_id):
    return get_application_jsonb_blob(application_id)


@assessment_assessment_bp.get("/application_fields_export/<fund_id>/<round_id>/<report_type>")
def get_application_data_for_export(fund_id: str, round_id: str, report_type: str) -> List[Dict]:
    """Fetch application data for export, prioritizing round-specific data if available."""

    round_data = applicant_info_mapping.get(f"{fund_id}:{round_id}") or applicant_info_mapping.get(fund_id, {})

    app_list = get_assessment_export_data(
        fund_id=fund_id,
        round_id=round_id,
        report_type=report_type,
        list_of_fields=round_data,
    )

    return app_list
