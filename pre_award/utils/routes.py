import os
from datetime import datetime, timedelta

from flask import current_app, jsonify, request
from sqlalchemy import or_

from pre_award.application_store.db.models.application.applications import Applications
from pre_award.application_store.db.models.feedback.end_of_application_survey import EndOfApplicationSurveyFeedback
from pre_award.application_store.db.models.feedback.feedback import Feedback
from pre_award.application_store.db.models.forms.forms import Forms
from pre_award.assessment_store.db.models.assessment_record.assessment_records import AssessmentRecord
from pre_award.common.blueprints import Blueprint
from pre_award.db import db

utils_bp = Blueprint("utils_bp", __name__)


def check_basic_auth():
    """Verify basic auth credentials"""
    auth = request.authorization
    if not auth:
        return False
    expected_username = os.environ.get("BASIC_AUTH_USERNAME")
    expected_password = os.environ.get("BASIC_AUTH_PASSWORD")
    if not expected_username or not expected_password:
        current_app.logger.error(
            "Basic auth credentials not configured in environment (BASIC_AUTH_USERNAME/BASIC_AUTH_PASSWORD)"
        )
        return False

    return auth.username == expected_username and auth.password == expected_password


def check_user_agent():
    """Validate User-Agent header."""
    user_agent = request.headers.get("User-Agent", "").lower()
    allowed_agents = ["curl", "github-actions", "python-requests"]
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
    - Basic auth
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

    BATCH_SIZE = 200  # Adjust based on DB performance
    try:
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

        # Count total records for logging
        apps_found = (
            db.session.query(Applications).filter(e2e_filter_apps, Applications.started_at < cutoff_time).count()
        )
        assessments_found = db.session.query(AssessmentRecord).filter(e2e_filter_assessments).count()

        current_app.logger.info(
            "E2E Cleanup started: Found %(apps)s applications, %(assessments)s assessments",
            dict(apps=apps_found, assessments=assessments_found),
        )

        # Delete applications and child records in batches (first)
        apps_deleted = 0
        while True:
            apps_batch = (
                db.session.query(Applications)
                .filter(e2e_filter_apps, Applications.started_at < cutoff_time)
                .limit(BATCH_SIZE)
                .all()
            )
            if not apps_batch:
                break

            app_ids = [app.id for app in apps_batch]

            # Delete child records directly via SQL
            db.session.query(EndOfApplicationSurveyFeedback).filter(
                EndOfApplicationSurveyFeedback.application_id.in_(app_ids)
            ).delete(synchronize_session=False)
            db.session.query(Feedback).filter(Feedback.application_id.in_(app_ids)).delete(synchronize_session=False)
            db.session.query(Forms).filter(Forms.application_id.in_(app_ids)).delete(synchronize_session=False)

            # Delete applications
            db.session.query(Applications).filter(Applications.id.in_(app_ids)).delete(synchronize_session=False)
            db.session.commit()
            apps_deleted += len(apps_batch)

        # Delete assessment records in batches (after applications)
        assessments_deleted = 0
        while True:
            batch = db.session.query(AssessmentRecord).filter(e2e_filter_assessments).limit(BATCH_SIZE).all()
            if not batch:
                break
            db.session.query(AssessmentRecord).filter(AssessmentRecord.id.in_([r.id for r in batch])).delete(
                synchronize_session=False
            )
            db.session.commit()
            assessments_deleted += len(batch)

        current_app.logger.info(
            "E2E Cleanup completed: Found %(apps_found)d applications, deleted %(apps_deleted)d; "
            "Found %(assessments_found)d assessments, deleted %(assessments_deleted)d",
            dict(
                apps_found=apps_found,
                apps_deleted=apps_deleted,
                assessments_found=assessments_found,
                assessments_deleted=assessments_deleted,
            ),
        )

        return jsonify(
            {
                "success": True,
                "applications_found": apps_found,
                "applications_deleted": apps_deleted,
                "assessments_found": assessments_found,
                "assessments_deleted": assessments_deleted,
                "timestamp": datetime.now().isoformat(),
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("E2E Cleanup failed: %(error)s", dict(error=str(e)))
        return jsonify({"success": False, "error": f"Failed to cleanup E2E data: {str(e)}"}), 500
