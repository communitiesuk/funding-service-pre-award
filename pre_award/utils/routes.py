from datetime import datetime, timedelta

from flask import jsonify
from sqlalchemy import text

from pre_award.common.blueprints import Blueprint
from pre_award.db import db

utils_bp = Blueprint("utils_bp", __name__)


@utils_bp.post("/cleanup-e2e-data")
def cleanup_e2e_data():
    """
    API endpoint to clean up E2E test data.

    Returns:
        JSON response with cleanup results
    """
    try:
        cutoff_time = datetime.now() - timedelta(hours=1)

        e2e_condition = """(project_name ILIKE '%e2e%'
                           OR project_name ILIKE '%Project e2e%'
                           OR project_name ILIKE '%Community Ownership Fund E2E Journey%'
                           OR project_name ILIKE '%COF EOI Automated E2E Test%')"""

        # Count before deleting
        total_apps_to_delete = db.session.execute(
            text(f"SELECT COUNT(*) FROM applications WHERE {e2e_condition} AND started_at < :cutoff"),
            {"cutoff": cutoff_time},
        ).scalar()

        total_assessments_to_delete = db.session.execute(
            text(f"SELECT COUNT(*) FROM assessment_records WHERE {e2e_condition}")
        ).scalar()

        # Delete assessment records and their children
        assess_subq = f"SELECT application_id FROM assessment_records WHERE {e2e_condition}"

        db.session.execute(text(f"DELETE FROM tag_association WHERE application_id IN ({assess_subq})"))
        db.session.execute(text(f"DELETE FROM scores WHERE application_id IN ({assess_subq})"))
        db.session.execute(text(f"DELETE FROM qa_complete WHERE application_id IN ({assess_subq})"))
        db.session.execute(
            text(
                f"DELETE FROM comments_update WHERE comment_id IN "
                f"(SELECT comment_id FROM comments WHERE application_id IN ({assess_subq}))"
            )
        )
        db.session.execute(text(f"DELETE FROM comments WHERE application_id IN ({assess_subq})"))
        db.session.execute(
            text(
                f"DELETE FROM flag_update WHERE assessment_flag_id IN "
                f"(SELECT id FROM assessment_flag WHERE application_id IN ({assess_subq}))"
            )
        )
        db.session.execute(text(f"DELETE FROM assessment_flag WHERE application_id IN ({assess_subq})"))
        db.session.execute(text(f"DELETE FROM allocation_association WHERE application_id IN ({assess_subq})"))

        deleted_assessments = db.session.execute(text(f"DELETE FROM assessment_records WHERE {e2e_condition}")).rowcount

        # Delete applications and their children
        app_subq = f"SELECT id FROM applications WHERE {e2e_condition} AND started_at < :cutoff"

        db.session.execute(
            text(f"DELETE FROM research_survey WHERE application_id IN ({app_subq})"), {"cutoff": cutoff_time}
        )
        db.session.execute(text(f"DELETE FROM forms WHERE application_id IN ({app_subq})"), {"cutoff": cutoff_time})
        db.session.execute(text(f"DELETE FROM feedback WHERE application_id IN ({app_subq})"), {"cutoff": cutoff_time})
        db.session.execute(
            text(f"DELETE FROM end_of_application_survey_feedback WHERE application_id IN ({app_subq})"),
            {"cutoff": cutoff_time},
        )
        db.session.execute(
            text(f"DELETE FROM eligibility WHERE application_id IN ({app_subq})"), {"cutoff": cutoff_time}
        )

        deleted_apps = db.session.execute(
            text(f"DELETE FROM applications WHERE {e2e_condition} AND started_at < :cutoff"), {"cutoff": cutoff_time}
        ).rowcount

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "applications_found": total_apps_to_delete,
                "assessments_found": total_assessments_to_delete,
                "applications_deleted": deleted_apps,
                "assessments_deleted": deleted_assessments,
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": f"Failed to cleanup E2E data: {str(e)}"}), 500
