import os
from datetime import datetime, timedelta

from flask import current_app, jsonify, request
from sqlalchemy import or_

from pre_award.application_store.db.models.application.applications import Applications
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.common.blueprints import Blueprint
from pre_award.db import db

utils_bp = Blueprint("utils_bp", __name__)


def check_basic_auth():
    """Verify basic authentication credentials using existing system."""
    auth = request.authorization
    if not auth:
        return False

    # Use environment variables that match GitHub Actions secrets
    expected_username = os.environ.get("FS_BASIC_AUTH_USERNAME")
    expected_password = os.environ.get("FS_BASIC_AUTH_PASSWORD")
    if not expected_username or not expected_password:
        current_app.logger.error(
            "Basic auth credentials not configured in environment (FS_BASIC_AUTH_USERNAME/FS_BASIC_AUTH_PASSWORD)"
        )
        return False

    return auth.username == expected_username and auth.password == expected_password


def check_user_agent():
    """Validate User-Agent header."""
    user_agent = request.headers.get("User-Agent", "").lower()
    allowed_agents = ["curl", "github-actions", "python-requests", "postman"]
    return any(agent in user_agent for agent in allowed_agents)


def check_environment():
    """Allow execution in development, test, and UAT environments."""
    env = os.environ.get("FLASK_ENV", "test")
    return env in ["development", "dev", "test", "uat"]


@utils_bp.post("/cleanup-e2e-data")
def cleanup_e2e_data():
    """
    Secure API endpoint to clean up E2E test data.

    Security layers:
    - Basic authentication
    - User-Agent validation
    - GitHub Actions header verification
    - Environment restriction
    - Comprehensive logging

    Returns:
        JSON response with cleanup results
    """
    # Log all cleanup attempts
    current_app.logger.info(
        "E2E Cleanup attempt from IP: %(ip)s, User-Agent: %(user_agent)s, GitHub-Header: %(github_header)s",
        dict(
            ip=request.remote_addr,
            user_agent=request.headers.get("User-Agent", "None"),
            github_header=request.headers.get("X-GitHub-Actions", "None"),
        ),
    )

    # Environment check
    if not check_environment():
        current_app.logger.error("E2E Cleanup blocked: Not in allowed environment")
        return jsonify({"success": False, "error": "Not available in this environment"}), 403

    # Basic Auth
    if not check_basic_auth():
        current_app.logger.error("E2E Cleanup blocked: Invalid authentication")
        return jsonify({"success": False, "error": "Authentication required"}), 401

    #  User-Agent validation
    if not check_user_agent():
        current_app.logger.error(
            "E2E Cleanup blocked: Invalid User-Agent: %(user_agent)s",
            dict(user_agent=request.headers.get("User-Agent")),
        )
        return jsonify({"success": False, "error": "Invalid user agent"}), 403

    # GitHub Actions verification (required in production)
    env = os.environ.get("FLASK_ENV", "test")
    if env not in ["development", "dev"] and request.headers.get("X-GitHub-Actions") != "cleanup-e2e":
        current_app.logger.error(
            "E2E Cleanup blocked: Invalid GitHub header: %(header)s",
            dict(header=request.headers.get("X-GitHub-Actions")),
        )
        return jsonify({"success": False, "error": "Invalid request source"}), 403

    try:
        # Time-based safety (1-hour cutoff)
        cutoff_time = datetime.now() - timedelta(hours=1)

        # E2E test data filter
        e2e_filter = or_(
            Applications.project_name.ilike("%e2e%"),
            Applications.project_name.ilike("%Project e2e%"),
            Applications.project_name.ilike("%Community Ownership Fund E2E Journey%"),
            Applications.project_name.ilike("%COF EOI Automated E2E Test%"),
        )

        assessment_e2e_filter = or_(
            AssessmentRecord.project_name.ilike("%e2e%"),
            AssessmentRecord.project_name.ilike("%Project e2e%"),
            AssessmentRecord.project_name.ilike("%Community Ownership Fund E2E Journey%"),
            AssessmentRecord.project_name.ilike("%COF EOI Automated E2E Test%"),
        )

        # Get applications to delete
        applications = db.session.query(Applications).filter(e2e_filter, Applications.started_at < cutoff_time).all()

        # Get assessment records to delete
        assessment_records = db.session.query(AssessmentRecord).filter(assessment_e2e_filter).all()

        # Count found records
        apps_found = len(applications)
        assessments_found = len(assessment_records)

        # Delete child records first to avoid foreign key violations
        for app in applications:
            for survey in app.end_of_application_survey:
                db.session.delete(survey)
            for feedback in app.feedbacks:
                db.session.delete(feedback)
            for form in app.forms:
                db.session.delete(form)

        # Delete assessment records
        for record in assessment_records:
            db.session.delete(record)

        # delete applications
        for app in applications:
            db.session.delete(app)

        db.session.commit()

        # Log successful cleanup
        current_app.logger.info(
            "E2E Cleanup completed successfully: Found and deleted %(apps)s applications, %(assessments)s assessments",
            dict(apps=apps_found, assessments=assessments_found),
        )

        return jsonify(
            {
                "success": True,
                "applications_found": apps_found,
                "applications_deleted": apps_found,
                "assessments_found": assessments_found,
                "assessments_deleted": assessments_found,
                "timestamp": datetime.now().isoformat(),
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("E2E Cleanup failed: %(error)s", dict(error=str(e)))
        return jsonify({"success": False, "error": f"Failed to cleanup E2E data: {str(e)}"}), 500
