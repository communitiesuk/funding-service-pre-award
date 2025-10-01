import hashlib
import json
import re

from flask import current_app, request
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound

from pre_award.common.blueprints import Blueprint
from pre_award.form_store.db.queries import (
    create_or_update_form,
    get_all_forms,
    get_form_by_url_path,
    publish_form,
)

form_store_bp = Blueprint("form_store_bp", __name__)


def _sanitise_for_logging(value):
    """Sanitise user input for safe logging by removing potentially dangerous characters"""
    if not isinstance(value, str):
        value = str(value)
    return re.sub(r"[^\w\-_.]", "", value)


def generate_form_hash(form_json):
    """Generate a consistent hash for form JSON data with sorted keys"""
    json_string = json.dumps(form_json, sort_keys=True, separators=(",", ":"))
    return hashlib.md5(json_string.encode()).hexdigest()


class FormsView(MethodView):
    def get(self):
        """GET /forms - Returns a list of all forms"""
        try:
            forms = get_all_forms()
            return [form.as_dict() for form in forms], 200
        except Exception as e:
            current_app.logger.error("Error retrieving forms: %s", str(e))
            return {"error": "Failed to retrieve forms"}, 500

    def post(self):
        """POST /forms - Creates or updates a form"""
        try:
            if not request.is_json:
                return {"error": "Request must be JSON with Content-Type: application/json"}, 400

            data = request.get_json()

            if not data or "url_path" not in data or "form_json" not in data:
                return {"error": "Missing required fields: url_path, form_json"}, 400

            url_path = data["url_path"]
            display_name = data.get("display_name")  # Optional field
            form_json = data["form_json"]

            # Validate that url_path is not empty or whitespace-only
            if not url_path or not url_path.strip():
                return {"error": "Form URL path cannot be empty"}, 400

            # Validate that form_json is valid JSON if it's a string
            if isinstance(form_json, str):
                try:
                    form_json = json.loads(form_json)
                except json.JSONDecodeError:
                    return {"error": "Invalid JSON in form_json field"}, 400

            form = create_or_update_form(url_path, display_name, form_json)
            current_app.logger.info("Form %s created/updated successfully", _sanitise_for_logging(url_path))

            return form.as_dict_with_draft_json(), 201

        except Exception as e:
            current_app.logger.error("Error creating/updating form: %s", str(e))
            return {"error": "Failed to create/update form"}, 500


class FormDraftView(MethodView):
    def get(self, url_path):
        """GET /forms/{url_path}/draft - Returns the draft_json object"""
        try:
            form = get_form_by_url_path(url_path)
            return form.as_dict_with_draft_json(), 200
        except NoResultFound:
            return {"error": f"Form '{url_path}' not found"}, 404
        except Exception as e:
            current_app.logger.error("Error retrieving draft for form %s: %s", _sanitise_for_logging(url_path), str(e))
            return {"error": "Failed to retrieve form draft"}, 500


class FormPublishedView(MethodView):
    def get(self, url_path):
        """GET /forms/{url_path}/published - Returns the published_json object"""
        try:
            form = get_form_by_url_path(url_path)
            if not form.published_json or form.published_json == {}:
                return {"error": f"Form '{url_path}' has not been published"}, 404
            response = form.as_dict_with_published_json()
            response["hash"] = generate_form_hash(form.published_json)
            return response, 200
        except NoResultFound:
            return {"error": f"Form '{url_path}' not found"}, 404
        except Exception as e:
            current_app.logger.error("Error retrieving published form %s: %s", _sanitise_for_logging(url_path), str(e))
            return {"error": "Failed to retrieve published form"}, 500


class FormHashView(MethodView):
    def get(self, url_path):
        """GET /forms/{url_path}/hash - Returns hash of published_json for cache validation"""
        try:
            form = get_form_by_url_path(url_path)
            if not form.published_json or form.published_json == {}:
                return {"error": f"Form '{url_path}' has not been published"}, 404
            return {"hash": generate_form_hash(form.published_json)}, 200
        except NoResultFound:
            return {"error": f"Form '{url_path}' not found"}, 404
        except Exception as e:
            current_app.logger.error("Error retrieving hash for form %s: %s", _sanitise_for_logging(url_path), str(e))
            return {"error": "Failed to retrieve form hash"}, 500


class FormPublishView(MethodView):
    def put(self, url_path):
        """PUT /forms/{url_path}/publish - Publishes a form (copies draft to published)"""
        try:
            form = publish_form(url_path)
            current_app.logger.info("Form %s published successfully", _sanitise_for_logging(url_path))
            return form.as_dict_with_published_json(), 200
        except NoResultFound:
            return {"error": f"Form '{url_path}' not found"}, 404
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            current_app.logger.error("Error publishing form %s: %s", _sanitise_for_logging(url_path), str(e))
            return {"error": "Failed to publish form"}, 500


# Register URL rules
form_store_bp.add_url_rule("", view_func=FormsView.as_view("forms"))
form_store_bp.add_url_rule("/<url_path>/draft", view_func=FormDraftView.as_view("form_draft"))
form_store_bp.add_url_rule("/<url_path>/published", view_func=FormPublishedView.as_view("form_published"))
form_store_bp.add_url_rule("/<url_path>/hash", view_func=FormHashView.as_view("form_hash"))
form_store_bp.add_url_rule("/<url_path>/publish", view_func=FormPublishView.as_view("form_publish"))
