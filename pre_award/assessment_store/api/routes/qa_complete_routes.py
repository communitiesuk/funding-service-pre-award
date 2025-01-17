from assessment_store.db.queries.assessment_records.queries import get_metadata_for_application
from assessment_store.db.queries.qa_complete.queries import (
    create_qa_complete_record,
    get_qa_complete_record_for_application,
)
from common.blueprints import Blueprint

assessment_qa_bp = Blueprint("assessment_qa_bp", __name__)


@assessment_qa_bp.post("/qa_complete/<application_id>/<user_id>")
def post_qa_complete_for_application(application_id: str, user_id: str):
    application_json = get_metadata_for_application(application_id)
    application_workflow_status = application_json.get("workflow_status")
    if application_workflow_status == "COMPLETED" and not get_qa_complete_record_for_application(application_id):
        created_qa_complete_record = create_qa_complete_record(
            application_id=application_id,
            user_id=user_id,
        )
        return created_qa_complete_record
    return {
        "code": 401,
        "message": f"Could not create qa_complete record for application with id: {application_id}",
        "status": "error",
    }, 401


@assessment_qa_bp.get("/qa_complete/<application_id>")
def qa_complete_record_for_application(application_id: str) -> dict:
    qa_complete_record = get_qa_complete_record_for_application(application_id)

    return qa_complete_record
