"""
Tests for form_store API routes.
"""

import json
from unittest.mock import patch


class TestFormsView:
    """Tests for the /forms endpoint."""

    def test_get_all_forms_empty(self, flask_test_client):
        """Test GET /forms returns empty list when no forms exist."""
        with patch("pre_award.form_store.api.routes.get_all_forms", return_value=[]):
            response = flask_test_client.get("/forms")

            assert response.status_code == 200
            assert response.json == []

    def test_get_all_forms_with_data(self, flask_test_client, multiple_form_records):
        """Test GET /forms returns all forms."""
        response = flask_test_client.get("/forms")

        assert response.status_code == 200
        assert len(response.json) == 3

        # Check form names are present
        form_names = [form["name"] for form in response.json]
        assert "form-1" in form_names
        assert "form-2" in form_names
        assert "form-3" in form_names

        # Check structure includes required fields
        for form in response.json:
            assert "id" in form
            assert "name" in form
            assert "draft_json" not in form
            assert "published_json" not in form
            assert "is_published" in form
            assert "created_at" in form
            assert "updated_at" in form

    def test_get_all_forms_error(self, flask_test_client):
        """Test GET /forms handles database errors."""
        with patch("pre_award.form_store.api.routes.get_all_forms", side_effect=Exception("Database error")):
            response = flask_test_client.get("/forms")

            assert response.status_code == 500
            assert response.json == {"error": "Failed to retrieve forms"}

    def test_post_create_form_success(self, flask_test_client, sample_form_data):
        """Test POST /forms creates a new form."""
        response = flask_test_client.post("/forms", data=json.dumps(sample_form_data), content_type="application/json")

        assert response.status_code == 201
        assert response.json["name"] == sample_form_data["name"]
        assert response.json["draft_json"] == sample_form_data["form_json"]
        assert response.json["published_json"] == {}
        assert response.json["is_published"] is False

    def test_post_update_existing_form(self, flask_test_client, sample_form_record):
        """Test POST /forms updates existing form."""
        updated_data = {
            "name": sample_form_record.name,
            "form_json": {
                "pages": [{"path": "/updated-page", "title": "Updated Page", "components": []}],
                "startPage": "/updated-page",
            },
        }

        response = flask_test_client.post("/forms", data=json.dumps(updated_data), content_type="application/json")

        assert response.status_code == 201
        assert response.json["name"] == updated_data["name"]
        assert response.json["draft_json"] == updated_data["form_json"]

    def test_post_missing_required_fields(self, flask_test_client):
        """Test POST /forms with missing required fields."""
        # Missing form_json
        response = flask_test_client.post(
            "/forms", data=json.dumps({"name": "test-form"}), content_type="application/json"
        )

        assert response.status_code == 400
        assert "Missing required fields" in response.json["error"]

    def test_post_invalid_json_string(self, flask_test_client):
        """Test POST /forms with invalid JSON string in form_json."""
        response = flask_test_client.post(
            "/forms",
            data=json.dumps({"name": "test-form", "form_json": "invalid json string"}),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert "Invalid JSON in form_json field" in response.json["error"]

    def test_post_no_json_body(self, flask_test_client):
        """Test POST /forms with no JSON body."""
        response = flask_test_client.post("/forms")

        assert response.status_code == 400
        assert "Missing required fields" in response.json["error"]

    def test_post_error_handling(self, flask_test_client, sample_form_data):
        """Test POST /forms handles database errors."""
        with patch("pre_award.form_store.api.routes.create_or_update_form", side_effect=Exception("Database error")):
            response = flask_test_client.post(
                "/forms", data=json.dumps(sample_form_data), content_type="application/json"
            )

            assert response.status_code == 500
            assert response.json == {"error": "Failed to create/update form"}

    def test_post_empty_name(self, flask_test_client):
        """Test POST /forms with empty or whitespace-only name."""
        # Test empty string
        response = flask_test_client.post(
            "/forms", data=json.dumps({"name": "", "form_json": {"test": "data"}}), content_type="application/json"
        )
        assert response.status_code == 400
        assert response.json["error"] == "Form name cannot be empty"

        # Test whitespace-only string
        response = flask_test_client.post(
            "/forms", data=json.dumps({"name": "   ", "form_json": {"test": "data"}}), content_type="application/json"
        )
        assert response.status_code == 400
        assert response.json["error"] == "Form name cannot be empty"


class TestFormDraftView:
    """Tests for the /forms/{name}/draft endpoint."""

    def test_get_draft_success(self, flask_test_client, sample_form_record):
        """Test GET /forms/{name}/draft returns draft JSON."""
        response = flask_test_client.get(f"/forms/{sample_form_record.name}/draft")

        assert response.status_code == 200
        assert response.json == sample_form_record.draft_json

    def test_get_draft_not_found(self, flask_test_client):
        """Test GET /forms/{name}/draft with non-existent form."""
        response = flask_test_client.get("/forms/non-existent-form/draft")

        assert response.status_code == 404
        assert "not found" in response.json["error"]

    def test_get_draft_error(self, flask_test_client):
        """Test GET /forms/{name}/draft handles database errors."""
        with patch("pre_award.form_store.api.routes.get_form_by_name", side_effect=Exception("Database error")):
            response = flask_test_client.get("/forms/test-form/draft")

            assert response.status_code == 500
            assert response.json == {"error": "Failed to retrieve form draft"}


class TestFormPublishedView:
    """Tests for the /forms/{name}/published endpoint."""

    def test_get_published_success(self, flask_test_client, published_form_record):
        """Test GET /forms/{name}/published returns published JSON."""
        response = flask_test_client.get(f"/forms/{published_form_record.name}/published")

        assert response.status_code == 200
        assert "configuration" in response.json
        assert "hash" in response.json
        assert response.json["configuration"] == published_form_record.published_json
        assert isinstance(response.json["hash"], str)
        assert len(response.json["hash"]) == 32  # MD5 hash length

    def test_get_published_not_published(self, flask_test_client, sample_form_record):
        """Test GET /forms/{name}/published with unpublished form."""
        response = flask_test_client.get(f"/forms/{sample_form_record.name}/published")

        assert response.status_code == 404
        assert "has not been published" in response.json["error"]

    def test_get_published_not_found(self, flask_test_client):
        """Test GET /forms/{name}/published with non-existent form."""
        response = flask_test_client.get("/forms/non-existent-form/published")

        assert response.status_code == 404
        assert "not found" in response.json["error"]

    def test_get_published_error(self, flask_test_client):
        """Test GET /forms/{name}/published handles database errors."""
        with patch("pre_award.form_store.api.routes.get_form_by_name", side_effect=Exception("Database error")):
            response = flask_test_client.get("/forms/test-form/published")

            assert response.status_code == 500
            assert response.json == {"error": "Failed to retrieve published form"}


class TestFormHashView:
    """Tests for the /forms/{name}/hash endpoint."""

    def test_get_hash_success(self, flask_test_client, published_form_record):
        """Test GET /forms/{name}/hash returns hash of published JSON."""
        response = flask_test_client.get(f"/forms/{published_form_record.name}/hash")

        assert response.status_code == 200
        assert "hash" in response.json
        assert isinstance(response.json["hash"], str)
        assert len(response.json["hash"]) == 32  # MD5 hash length

    def test_get_hash_not_published(self, flask_test_client, sample_form_record):
        """Test GET /forms/{name}/hash with unpublished form."""
        response = flask_test_client.get(f"/forms/{sample_form_record.name}/hash")

        assert response.status_code == 404
        assert "has not been published" in response.json["error"]

    def test_get_hash_not_found(self, flask_test_client):
        """Test GET /forms/{name}/hash with non-existent form."""
        response = flask_test_client.get("/forms/non-existent-form/hash")

        assert response.status_code == 404
        assert "not found" in response.json["error"]

    def test_get_hash_error(self, flask_test_client):
        """Test GET /forms/{name}/hash handles database errors."""
        with patch("pre_award.form_store.api.routes.get_form_by_name", side_effect=Exception("Database error")):
            response = flask_test_client.get("/forms/test-form/hash")

            assert response.status_code == 500
            assert response.json == {"error": "Failed to retrieve form hash"}

    def test_get_hash_consistency(self, flask_test_client, published_form_record):
        """Test hash is consistent for same published JSON."""
        response1 = flask_test_client.get(f"/forms/{published_form_record.name}/hash")
        response2 = flask_test_client.get(f"/forms/{published_form_record.name}/hash")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json["hash"] == response2.json["hash"]


class TestFormPublishView:
    """Tests for the /forms/{name}/publish endpoint."""

    def test_publish_form_success(self, flask_test_client, sample_form_record):
        """Test PUT /forms/{name}/publish publishes a form."""
        response = flask_test_client.put(f"/forms/{sample_form_record.name}/publish")

        assert response.status_code == 200
        assert response.json["name"] == sample_form_record.name
        assert response.json["published_json"] == sample_form_record.draft_json
        assert response.json["is_published"] is True
        assert response.json["published_at"] is not None

    def test_publish_form_not_found(self, flask_test_client):
        """Test PUT /forms/{name}/publish with non-existent form."""
        response = flask_test_client.put("/forms/non-existent-form/publish")

        assert response.status_code == 404
        assert "not found" in response.json["error"]

    def test_publish_form_no_draft(self, flask_test_client):
        """Test PUT /forms/{name}/publish with form having no draft."""
        with patch(
            "pre_award.form_store.api.routes.publish_form",
            side_effect=ValueError('Form "test" has no draft to publish'),
        ):
            response = flask_test_client.put("/forms/test-form/publish")

            assert response.status_code == 400
            assert "has no draft to publish" in response.json["error"]

    def test_publish_form_error(self, flask_test_client):
        """Test PUT /forms/{name}/publish handles database errors."""
        with patch("pre_award.form_store.api.routes.publish_form", side_effect=Exception("Database error")):
            response = flask_test_client.put("/forms/test-form/publish")

            assert response.status_code == 500
            assert response.json == {"error": "Failed to publish form"}
