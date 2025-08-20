"""
Simple decorators for fund store API endpoints
"""

from functools import wraps

from flask import current_app, jsonify


def development_only(f):
    """
    Decorator to block endpoints in production environments.
    Only allows access in development, dev, test, unit_test environments.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        flask_env = current_app.config.get("FLASK_ENV", "").lower()
        if flask_env not in ["development", "dev", "test", "unit_test"]:
            current_app.logger.warning(
                "Development-only endpoint %s called in %s environment - blocked", f.__name__, flask_env
            )
            return jsonify({"error": "This endpoint is disabled in production environments"}), 403
        return f(*args, **kwargs)

    return decorated_function
