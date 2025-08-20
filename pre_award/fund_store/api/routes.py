import uuid
from datetime import datetime
from distutils.util import strtobool

from flask import abort, current_app, jsonify, request
from fsd_utils.locale_selector.get_lang import get_lang

from data.models import Round
from pre_award.common.blueprints import Blueprint
from pre_award.db import db
from pre_award.fund_store.db.models.event import EventType
from pre_award.fund_store.db.queries import create_event as create_event_in_db
from pre_award.fund_store.db.queries import (
    get_all_funds,
    get_application_sections_for_round,
    get_assessment_sections_for_round,
    get_fund_by_id,
    get_fund_by_short_name,
    get_round_by_id,
    get_round_by_short_name,
    get_rounds_for_fund_by_id,
    get_rounds_for_fund_by_short_name,
)
from pre_award.fund_store.db.queries import get_event as get_event_from_db
from pre_award.fund_store.db.queries import get_events as get_events_from_db
from pre_award.fund_store.db.queries import set_event_to_processed as set_event_to_processed_in_db
from pre_award.fund_store.db.schemas.event import EventSchema
from pre_award.fund_store.db.schemas.fund import FundSchema
from pre_award.fund_store.db.schemas.round import RoundSchema
from pre_award.fund_store.db.schemas.section import SECTION_SCHEMA_MAP
from pre_award.fund_store.decorators import development_only
from pre_award.fund_store.services.fab_import_service import transform_fund_configuration
from pre_award.fund_store.services.save_fund_configuration import process_fund_config

fund_store_bp = Blueprint("fund_store_bp", __name__)


def is_valid_uuid(value):
    try:
        obj = uuid.UUID(value)
        return str(obj) == value.lower()
    except Exception:
        return False


def is_valid_isoformat_datetime(datetime_str):
    try:
        datetime.fromisoformat(datetime_str)
    except Exception:
        return False
    return True


def filter_fund_by_lang(fund_data, lang_key: str = "en"):
    def filter_fund(data):
        data["name"] = data["name_json"].get(lang_key) or data["name_json"]["en"]
        data["title"] = data["title_json"].get(lang_key) or data["title_json"]["en"]
        data["description"] = data["description_json"].get(lang_key) or data["description_json"]["en"]
        return data

    if isinstance(fund_data, dict):
        fund = filter_fund(fund_data)
    elif isinstance(fund_data, list):
        fund = [filter_fund(item) for item in fund_data]
    else:
        fund = fund_data

    return fund


def filter_round_by_lang(round_data, lang_key: str = "en"):
    def filter_round(data):
        data["title"] = data["title_json"].get(lang_key) or data["title_json"]["en"]
        data["instructions"] = (
            data["instructions_json"].get(lang_key) or data["instructions_json"].get("en")
            if data["instructions_json"]
            else ""
        )
        data["application_guidance"] = (
            data["application_guidance_json"].get(lang_key) or data["application_guidance_json"].get("en")
            if data["application_guidance_json"]
            else ""
        )
        return data

    if isinstance(round_data, dict):
        round = filter_round(round_data)
    elif isinstance(round_data, list):
        round = [filter_round(item) for item in round_data]
    else:
        round = round_data

    return round


@fund_store_bp.get("/funds")
def get_funds():
    language = request.args.get("language", "en").replace("?", "")
    funds = get_all_funds()

    if funds:
        serialiser = FundSchema()
        return jsonify(filter_fund_by_lang(fund_data=serialiser.dump(funds, many=True), lang_key=language))
    current_app.logger.warning("No funds were found, please check this.")
    return jsonify(funds)


@fund_store_bp.get("/funds/<fund_id>")
def get_fund(fund_id):
    language = request.args.get("language", "en").replace("?", "")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        fund = get_fund_by_short_name(fund_id) if fund_id else None
    else:
        fund = get_fund_by_id(fund_id) if is_valid_uuid(fund_id) else None

    if fund:
        serialiser = FundSchema()
        return jsonify(filter_fund_by_lang(fund_data=serialiser.dump(fund), lang_key=language))

    abort(404)


def get_round_from_db(fund_id, round_id) -> Round:
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        round = get_round_by_short_name(fund_id, round_id)
    else:
        round = get_round_by_id(fund_id, round_id) if is_valid_uuid(fund_id) and is_valid_uuid(round_id) else None
    return round


@fund_store_bp.get("/funds/<fund_id>/rounds/<round_id>")
def get_round(fund_id, round_id):
    round = get_round_from_db(fund_id, round_id)
    language = request.args.get("language", "en").replace("?", "")
    if round:
        serialiser = RoundSchema()
        return filter_round_by_lang(round_data=serialiser.dump(round), lang_key=language)

    abort(404)


@fund_store_bp.get("/funds/<fund_id>/rounds/<round_id>/eoi_decision_schema")
def get_eoi_deicision_schema_for_round(fund_id, round_id):
    language = request.args.get("language", "en").replace("?", "").lower()
    round = get_round_from_db(fund_id=fund_id, round_id=round_id)
    if not round:
        abort(404)

    if not round.eoi_decision_schema:
        return {}

    return round.eoi_decision_schema.get(language) or {}


@fund_store_bp.get("/funds/<fund_id>/rounds")
def get_rounds_for_fund(fund_id):
    language = request.args.get("language", "en").replace("?", "")
    short_name_arg = request.args.get("use_short_name")
    use_short_name = short_name_arg and strtobool(short_name_arg)

    if use_short_name:
        rounds = get_rounds_for_fund_by_short_name(fund_id)
    else:
        rounds = get_rounds_for_fund_by_id(fund_id) if is_valid_uuid(fund_id) else None

    if rounds:
        serialiser = RoundSchema()
        dumped = [serialiser.dump(r) for r in rounds]
        return filter_round_by_lang(round_data=dumped, lang_key=language)

    abort(404)


@fund_store_bp.get("/funds/<fund_id>/rounds/<round_id>/sections/application")
def get_sections_for_round_application(fund_id, round_id):
    language = request.args.get("language", "en").replace("?", "")
    if is_valid_uuid(fund_id) and is_valid_uuid(round_id):
        sections = get_application_sections_for_round(fund_id, round_id)
        if sections:
            section_schema = SECTION_SCHEMA_MAP.get(language)
            serialiser = section_schema()
            dumped = serialiser.dump(sections, many=True)
            return dumped
    abort(404)


@fund_store_bp.get("/funds/<fund_id>/rounds/<round_id>/sections/assessment")
def get_sections_for_round_assessment(fund_id, round_id):
    language = request.args.get("language", "en").replace("?", "")
    if is_valid_uuid(fund_id) and is_valid_uuid(round_id):
        sections = get_assessment_sections_for_round(fund_id, round_id, get_lang())
        if sections:
            section_schema = SECTION_SCHEMA_MAP.get(language)
            serialiser = section_schema()
            return serialiser.dump(sections, many=True)

    abort(404)


@fund_store_bp.post("/event")
def create_event():
    args = request.json
    if not args or "type" not in args:
        return jsonify({"detail": "Post body must contain event type field"}), 400

    if "activation_date" not in args or not is_valid_isoformat_datetime(args["activation_date"]):
        return jsonify({"detail": "Activation date must be in isoformat datetime"}), 400

    if "processed" in args and not (is_valid_isoformat_datetime(args["processed"])):
        return jsonify({"detail": "Processed field must be an isoformat datetime"}), 400

    if "round_id" in args and not is_valid_uuid(args["round_id"]):
        return jsonify({"detail": "Round ID must be a UUID"}), 400

    event = create_event_in_db(
        type=args["type"],
        activation_date=args["activation_date"],
        round_id=args.get("round_id"),
        processed=args.get("processed"),
    )

    if event:
        serialiser = EventSchema()
        return serialiser.dump(event), 201
    abort(500)


@fund_store_bp.get("/funds/<fund_id>/rounds/<round_id>/events")
def get_events_for_round(fund_id, round_id):
    if not is_valid_uuid(round_id):
        return jsonify({"detail": "One or more IDs is not of format UUID"}), 400

    only_unprocessed = request.args.get("only_unprocessed", False, type=lambda x: x.lower() == "true")
    events = get_events_from_db(round_id=round_id, only_unprocessed=only_unprocessed)
    if events:
        serialiser = EventSchema()
        return serialiser.dump(events, many=True)
    abort(404)


@fund_store_bp.get("/events/<type>")
def get_events_by_type(type):
    if not any(type == event_type.value for event_type in EventType):
        return jsonify({"detail": "Event type not recognised"}), 400
    only_unprocessed = request.args.get("only_unprocessed", False, type=lambda x: x.lower() == "true")
    events = get_events_from_db(type=type, only_unprocessed=only_unprocessed)
    if events:
        serialiser = EventSchema()
        return serialiser.dump(events, many=True)
    abort(404)


# TODO: deprecate in favour of get_event_by_id
@fund_store_bp.get("/funds/<fund_id>/rounds/<round_id>/event/<event_id>")
def get_event_for_round(fund_id, round_id, event_id):
    if not is_valid_uuid(event_id) or not is_valid_uuid(round_id):
        return jsonify({"detail": "One or more IDs is not of format UUID"}), 400

    event = get_event_from_db(round_id=round_id, event_id=event_id)
    if event:
        serialiser = EventSchema()
        return serialiser.dump(event)

    abort(404)


@fund_store_bp.get("/event/<event_id>")
def get_event_by_id(event_id):
    if not is_valid_uuid(event_id):
        return jsonify({"detail": "One or more IDs is not of format UUID"}), 400
    event = get_event_from_db(event_id=event_id)
    if event:
        serialiser = EventSchema()
        return serialiser.dump(event)
    abort(404)


@fund_store_bp.put("/funds/<fund_id>/rounds/<round_id>/event/<event_id>")
def set_round_event_to_processed(fund_id, round_id, event_id):
    if not is_valid_uuid(event_id) or not is_valid_uuid(round_id):
        return jsonify({"detail": "One or more IDs is not of format UUID"}), 400
    processed = request.args.get("processed", type=lambda x: x.lower() == "true")
    event = set_event_to_processed_in_db(event_id=event_id, processed=processed)
    if event:
        serialiser = EventSchema()
        return jsonify(serialiser.dump(event))
    abort(404)


@fund_store_bp.put("/event/<event_id>")
def set_event_to_processed(event_id):
    if not is_valid_uuid(event_id):
        return jsonify({"detail": "One or more IDs is not of format UUID"}), 400
    processed = request.args.get("processed", type=lambda x: x.lower() == "true")
    event = set_event_to_processed_in_db(event_id=event_id, processed=processed)
    if event:
        serialiser = EventSchema()
        return jsonify(serialiser.dump(event))
    abort(404)


@fund_store_bp.get("/funds/<fund_id>/rounds/<round_id>/available_flag_allocations")
def get_available_flag_allocations_endpoint(fund_id, round_id):
    return jsonify(get_available_flag_allocations(fund_id, round_id))


def get_available_flag_allocations(fund_id, round_id):
    # TODO: Currently teams are hardcoded, move it to database implementation
    from pre_award.assessment_store.config.mappings.assessment_mapping_fund_round import (
        CTDF_FUND_ID,
        CTDF_ROUND_1_ID,
    )
    from pre_award.fund_store.config.fund_loader_config.cof.cof_r2 import (
        COF_ROUND_2_WINDOW_2_ID,
        COF_ROUND_2_WINDOW_3_ID,
    )
    from pre_award.fund_store.config.fund_loader_config.cof.cof_r3 import (
        COF_FUND_ID,
        COF_ROUND_3_WINDOW_1_ID,
        COF_ROUND_3_WINDOW_2_ID,
        COF_ROUND_3_WINDOW_3_ID,
    )
    from pre_award.fund_store.config.fund_loader_config.cof.cof_r4 import COF_ROUND_4_WINDOW_1_ID
    from pre_award.fund_store.config.fund_loader_config.cyp.cyp_r1 import (
        CYP_FUND_ID,
        CYP_ROUND_1_ID,
    )
    from pre_award.fund_store.config.fund_loader_config.digital_planning.dpi_r2 import (
        DPI_FUND_ID,
        DPI_ROUND_2_ID,
    )
    from pre_award.fund_store.config.fund_loader_config.night_shelter.ns_r2 import (
        NIGHT_SHELTER_FUND_ID,
        NIGHT_SHELTER_ROUND_2_ID,
    )

    cof_teams = [
        {"key": "ASSESSOR", "value": "Assessor"},
        {"key": "COMMERCIAL_ASSESSOR", "value": "Commercial Assessor"},
        {"key": "LEAD_ASSESSOR", "value": "Lead Assessor"},
        {"key": "LEAD_COMMERCIAL_ASSESSOR", "value": "Lead Commercial Assessor"},
        {"key": "COF_POLICY", "value": "COF Policy"},
    ]

    nstf_teams = [
        {"key": "COMMERCIAL", "value": "Commercial"},
        {"key": "NSTF_TEAM", "value": "NSTF Team"},
        {"key": "HOUSING_JUSTICE", "value": "Housing Justice"},
        {"key": "HOMELESS_LINK", "value": "Homeless Link"},
        {"key": "RS_ADVISORS", "value": "RS Advisors"},
    ]

    cyp_teams = [
        {"key": "COMMERCIAL_ASSESSOR", "value": "Commercial Assessor"},
        {"key": "LEAD_ASSESSOR", "value": "Lead Assessor"},
    ]

    dpif_teams = [
        {"key": "ELIGIBILITY", "value": "Eligibility"},
        {"key": "MODERATION", "value": "Moderation"},
        {"key": "LEAD_ASSESSOR", "value": "Lead Assessor"},
    ]
    ctdf_teams = [  # ctdf is a dummy fund and the teams are also setup for the sake of demo
        {"key": "CTDF_TEAM", "value": "Funding Service"},
        {"key": "MODERATION", "value": "Moderation"},
        {"key": "LEAD_ASSESSOR", "value": "Lead Assessor"},
    ]
    if is_valid_uuid(fund_id) and is_valid_uuid(round_id):
        if fund_id == COF_FUND_ID and round_id in COF_ROUND_2_WINDOW_2_ID:
            return cof_teams
        elif fund_id == COF_FUND_ID and round_id == COF_ROUND_2_WINDOW_3_ID:
            return cof_teams
        elif fund_id == COF_FUND_ID and round_id == COF_ROUND_3_WINDOW_1_ID:
            return cof_teams
        elif fund_id == COF_FUND_ID and round_id == COF_ROUND_3_WINDOW_2_ID:
            return cof_teams
        elif fund_id == COF_FUND_ID and round_id == COF_ROUND_3_WINDOW_3_ID:
            return cof_teams
        elif fund_id == COF_FUND_ID and round_id == COF_ROUND_4_WINDOW_1_ID:
            return cof_teams
        elif fund_id == NIGHT_SHELTER_FUND_ID and round_id == NIGHT_SHELTER_ROUND_2_ID:
            return nstf_teams
        elif fund_id == CYP_FUND_ID and round_id == CYP_ROUND_1_ID:
            return cyp_teams
        elif fund_id == DPI_FUND_ID and round_id == DPI_ROUND_2_ID:
            return dpif_teams
        elif fund_id == CTDF_FUND_ID and round_id == CTDF_ROUND_1_ID:
            return ctdf_teams
    abort(404)


@fund_store_bp.put("/funds/<round_id>/application_reminder_status")
def update_application_reminder_sent_status(round_id):
    try:
        status = request.args.get("status")
        round_instance = Round.query.filter_by(id=round_id).first() if is_valid_uuid(round_id) else None

        if not round_instance:
            return jsonify({"message": "Round ID not found"}), 404
        reminder_status = round_instance.application_reminder_sent

        if status.lower() == "true" and reminder_status is False:
            round_instance.application_reminder_sent = True
            db.session.commit()
            (
                current_app.logger.info(
                    "application_reminder_sent status updated successfully",
                ),
                200,
            )
            return (
                jsonify({"message": f"application_reminder_sent status has been updated to True for round {round_id}"}),
                200,
            )
        else:
            return (
                jsonify({"message": "application_reminder_sent Status should be True"}),
                400,
            )

    except Exception as e:
        (
            current_app.logger.error(
                "The application_reminder_sent status could not be updated %(error)s",
                dict(error=str(e)),
            ),
            400,
        )
        return (
            jsonify({"message": f"The application_reminder_sent status could not be updated for round_id {round_id}"}),
            400,
        )


@fund_store_bp.post("/import-config")
@development_only
def import_fund_config():
    """
    API endpoint to import fund configuration from FAB and process it.
    Replaces the manual process of copying Python files and running scripts.
    """
    try:
        # Get JSON data from request
        fund_config_data = request.json

        if not fund_config_data:
            return jsonify({"error": "No JSON data provided"}), 400

        fund_short_name = fund_config_data.get("fund_config", {}).get("short_name", "")
        current_app.logger.info("Received fund config import request for: %s", fund_short_name)

        # Validate required fields for FAB export format
        required_fields = ["sections_config", "fund_config", "round_config", "base_path"]
        for field in required_fields:
            if field not in fund_config_data:
                current_app.logger.warning("Missing required field '%s' for fund: %s", field, fund_short_name)
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Convert FAB export format to internal format
        current_app.logger.info("Converting FAB export format to internal format for fund: %s", fund_short_name)
        processed_fund_data = transform_fund_configuration(fund_config_data)

        # Get the fund data from the transformed structure
        fund_short_name = list(processed_fund_data.keys())[0]
        fund_data = processed_fund_data[fund_short_name]

        result = process_fund_config(fund_data)
        if result["success"]:
            current_app.logger.info("Successfully processed fund config for fund: %s", fund_short_name)
            return jsonify({"message": result["message"]}), 201
        else:
            current_app.logger.error(
                "Failed to process fund config for fund %s: %s", fund_short_name, result["message"]
            )
            return jsonify({"error": result["message"]}), 500
    except Exception as e:
        current_app.logger.error("Error processing fund config: %s", str(e))
        return jsonify({"error": "Internal server error occurred while processing fund configuration"}), 500
