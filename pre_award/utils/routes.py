from flask import current_app, jsonify, request

from pre_award.common.blueprints import Blueprint
from pre_award.config import Config
from pre_award.utils.e2e_cleanup_service import delete_e2e_test_data

utils_bp = Blueprint("utils_bp", __name__)


@utils_bp.post("/e2e-test-data/cleanup")
def delete_e2e_test_data_route():
    "Trigger cleanup of E2E test data."

    # Log cleanup attempt
    current_app.logger.info(
        "E2E Cleanup attempt from IP: %(ip)s",
        {"ip": request.remote_addr},
    )

    # Environment check
    if Config.FLASK_ENV not in ["development", "dev", "test", "uat"]:
        current_app.logger.error("E2E Cleanup blocked: Not in allowed environment")
        return jsonify({"success": False, "error": "Not available in this environment"}), 403

    try:
        result = delete_e2e_test_data()
        return jsonify({"success": True, **result}), 200

    except Exception as e:
        current_app.logger.exception("E2E Cleanup failed: %(error)s", {"error": str(e)})
        return jsonify({"success": False, "error": str(e)}), 500
