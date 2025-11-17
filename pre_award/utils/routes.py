from datetime import datetime, timedelta

from flask import current_app, jsonify, request
from sqlalchemy import DateTime, cast, or_

from pre_award.application_store.db.models.application.applications import Applications
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.common.blueprints import Blueprint
from pre_award.config import Config
from pre_award.db import db

utils_bp = Blueprint("utils_bp", __name__)


def check_user_agent():
    """Validate User-Agent header."""
    user_agent = request.headers.get("User-Agent", "").lower()
    allowed_agents = ["curl", "github-actions", "python-requests", "postman"]
    return any(agent in user_agent for agent in allowed_agents)


def check_environment():
    """Allow execution in development, test, and UAT environments."""
    return Config.FLASK_ENV in ["development", "dev", "test", "uat"]


@utils_bp.post("/cleanup-e2e-data")
def cleanup_e2e_data():
    """
    Simple API endpoint to clean up E2E test data.
    Returns:
        JSON response with cleanup results
    """
    # Log cleanup attempt
    current_app.logger.info(
        "E2E Cleanup attempt from IP: %(ip)s, User-Agent: %(user_agent)s",
        dict(
            ip=request.remote_addr,
            user_agent=request.headers.get("User-Agent", "None"),
        ),
    )

    # Environment check
    if not check_environment():
        current_app.logger.error("E2E Cleanup blocked: Not in allowed environment")
        return jsonify({"success": False, "error": "Not available in this environment"}), 403

    # User-Agent validation
    if not check_user_agent():
        current_app.logger.error(
            "E2E Cleanup blocked: Invalid User-Agent: %(user_agent)s",
            dict(user_agent=request.headers.get("User-Agent")),
        )
        return jsonify({"success": False, "error": "Invalid user agent"}), 403

    try:
        result = cleanup_e2e_logic()
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.exception("E2E Cleanup failed: %(error)s", dict(error=str(e)))
        return jsonify({"success": False, "error": str(e)}), 500


def cleanup_e2e_logic():
    """Cleanup of E2E test data."""
    cutoff_time = datetime.now() - timedelta(hours=1)

    # E2E test filters
    e2e_filters = [
        "%e2e%",
        "%Project e2e%",
        "%Community Ownership Fund E2E Journey%",
        "%COF EOI Automated E2E Test%",
    ]
    e2e_filter_apps = or_(*[Applications.project_name.ilike(f) for f in e2e_filters])
    e2e_filter_assessments = or_(*[AssessmentRecord.project_name.ilike(f) for f in e2e_filters])

    # Get applications to delete
    applications = db.session.query(Applications).filter(e2e_filter_apps, Applications.started_at < cutoff_time).all()

    # Get assessment records to delete
    assessment_records = (
        db.session.query(AssessmentRecord)
        .filter(e2e_filter_assessments, cast(AssessmentRecord.date_submitted, DateTime) < cutoff_time)
        .all()
    )

    current_app.logger.info(
        "E2E Cleanup found %(apps)d applications, %(assessments)d assessments",
        dict(apps=len(applications), assessments=len(assessment_records)),
    )

    # Delete applications
    for app in applications:
        db.session.delete(app)

    # Delete assessment records
    for record in assessment_records:
        db.session.delete(record)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    current_app.logger.info(
        "E2E Cleanup completed: Deleted %(apps)d applications, %(assessments)d assessments",
        dict(apps=len(applications), assessments=len(assessment_records)),
    )

    return {
        "success": True,
        "applications_found": len(applications),
        "applications_deleted": len(applications),
        "assessments_found": len(assessment_records),
        "assessments_deleted": len(assessment_records),
        "timestamp": datetime.now().isoformat(),
    }
