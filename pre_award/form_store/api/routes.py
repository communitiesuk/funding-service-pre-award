import hashlib
import json

from flask import current_app, request
from flask.views import MethodView
from fsd_utils.authentication.decorators import login_required
from sqlalchemy.orm.exc import NoResultFound

from pre_award.common.blueprints import Blueprint
from pre_award.form_store.db.queries import (
    create_or_update_form,
    get_all_forms,
    get_form_by_name,
    publish_form,
)

form_store_bp = Blueprint("form_store_bp", __name__)


class FormsView(MethodView):
    decorators = [login_required]

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
                return {"error": "Missing required fields: name, form_json"}, 400

            data = request.get_json()

            if not data or "name" not in data or "form_json" not in data:
                return {"error": "Missing required fields: name, form_json"}, 400

            name = data["name"]
            form_json = data["form_json"]

            # Validate that form_json is valid JSON if it's a string
            if isinstance(form_json, str):
                try:
                    form_json = json.loads(form_json)
                except json.JSONDecodeError:
                    return {"error": "Invalid JSON in form_json field"}, 400

            form = create_or_update_form(name, form_json)
            current_app.logger.info("Form %s created/updated successfully", name)

            return form.as_dict(), 201

        except Exception as e:
            current_app.logger.error("Error creating/updating form: %s", str(e))
            return {"error": "Failed to create/update form"}, 500


class FormDraftView(MethodView):
    decorators = [login_required]

    def get(self, name):
        """GET /forms/{name}/draft - Returns the draft_json object"""
        try:
            form = get_form_by_name(name)
            return form.draft_json, 200
        except NoResultFound:
            return {"error": f"Form '{name}' not found"}, 404
        except Exception as e:
            current_app.logger.error("Error retrieving draft for form %s: %s", name, str(e))
            return {"error": "Failed to retrieve form draft"}, 500


class FormPublishedView(MethodView):
    decorators = [login_required]

    def get(self, name):
        """GET /forms/{name}/published - Returns the published_json object"""
        try:
            form = get_form_by_name(name)
            if not form.published_json or form.published_json == {}:
                return {"error": f"Form '{name}' has not been published"}, 404
            return form.published_json, 200
        except NoResultFound:
            return {"error": f"Form '{name}' not found"}, 404
        except Exception as e:
            current_app.logger.error("Error retrieving published form %s: %s", name, str(e))
            return {"error": "Failed to retrieve published form"}, 500


class FormHashView(MethodView):
    decorators = [login_required]

    def get(self, name):
        """GET /forms/{name}/hash - Returns hash of published_json for cache validation"""
        try:
            form = get_form_by_name(name)
            if not form.published_json or form.published_json == {}:
                return {"error": f"Form '{name}' has not been published"}, 404

            # Create hash of published_json
            json_string = json.dumps(form.published_json, sort_keys=True, separators=(",", ":"))
            hash_value = hashlib.md5(json_string.encode()).hexdigest()

            return {"hash": hash_value}, 200
        except NoResultFound:
            return {"error": f"Form '{name}' not found"}, 404
        except Exception as e:
            current_app.logger.error("Error retrieving hash for form %s: %s", name, str(e))
            return {"error": "Failed to retrieve form hash"}, 500


class FormPublishView(MethodView):
    decorators = [login_required]

    def put(self, name):
        """PUT /forms/{name}/publish - Publishes a form (copies draft to published)"""
        try:
            form = publish_form(name)
            current_app.logger.info("Form %s published successfully", name)
            return form.as_dict(), 200
        except NoResultFound:
            return {"error": f"Form '{name}' not found"}, 404
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            current_app.logger.error("Error publishing form %s: %s", name, str(e))
            return {"error": "Failed to publish form"}, 500


# Register URL rules
form_store_bp.add_url_rule("", view_func=FormsView.as_view("forms"))
form_store_bp.add_url_rule("/<name>/draft", view_func=FormDraftView.as_view("form_draft"))
form_store_bp.add_url_rule("/<name>/published", view_func=FormPublishedView.as_view("form_published"))
form_store_bp.add_url_rule("/<name>/hash", view_func=FormHashView.as_view("form_hash"))
form_store_bp.add_url_rule("/<name>/publish", view_func=FormPublishView.as_view("form_publish"))
