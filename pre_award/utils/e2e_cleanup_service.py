from datetime import datetime, timedelta

from flask import current_app
from sqlalchemy import DateTime, cast, text

from pre_award.application_store.db.models.application.applications import Applications
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.db import db


def delete_e2e_test_data():
    """Cleanup of E2E test data."""
    cutoff_time = datetime.now() - timedelta(hours=1)

    # Get applications to delete
    applications_to_delete = db.session.query(Applications).filter(
        Applications.project_name.ilike("%e2e%"),
        Applications.started_at < cutoff_time,
    )
    application_count = applications_to_delete.count()
    applications_to_delete.delete(synchronize_session=False)

    # Get assessment records to delete
    assessments_to_delete = db.session.query(AssessmentRecord).filter(
        AssessmentRecord.project_name.ilike("%e2e%"),
        text(
            """
                jsonb_typeof(jsonb_path_query_first(assessment_records.jsonb_blob, '$.date_submitted')) = 'string'
                """
        ),
        cast(text("jsonb_path_query_first(assessment_records.jsonb_blob, '$.date_submitted')::text"), DateTime)
        < cutoff_time,
    )
    assessment_count = assessments_to_delete.count()
    assessments_to_delete.delete(synchronize_session=False)

    current_app.logger.info(
        "E2E Cleanup found %(apps)d applications, %(assessments)d assessments",
        {"apps": application_count, "assessments": assessment_count},
    )
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    current_app.logger.info(
        "E2E Cleanup completed: Deleted %(apps)d applications, %(assessments)d assessments",
        {"apps": application_count, "assessments": assessment_count},
    )

    return {
        "applications_count": application_count,
        "assessments_count": assessment_count,
        "timestamp": datetime.now().isoformat(),
    }
