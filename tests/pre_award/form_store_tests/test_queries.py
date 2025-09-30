"""
Tests for form_store database queries.
"""

from datetime import datetime
from unittest.mock import patch

import pytest
from sqlalchemy.orm.exc import NoResultFound

from pre_award.form_store.db.models.form_definition import FormDefinition
from pre_award.form_store.db.queries import create_or_update_form, get_all_forms, get_form_by_url_path, publish_form


class TestGetAllForms:
    """Tests for get_all_forms query."""

    def test_get_all_forms_empty(self, db):
        """Test get_all_forms returns empty list when no forms exist."""
        result = get_all_forms()
        assert result == []

    def test_get_all_forms_with_data(self, db, multiple_form_records):
        """Test get_all_forms returns all forms."""
        result = get_all_forms()

        assert len(result) == 3
        form_url_paths = [form.url_path for form in result]
        assert "form-1" in form_url_paths
        assert "form-2" in form_url_paths
        assert "form-3" in form_url_paths


class TestGetFormByUrlPath:
    """Tests for get_form_by_url_path query."""

    def test_get_form_by_url_path_success(self, db, sample_form_record):
        """Test get_form_by_url_path returns correct form."""
        result = get_form_by_url_path(sample_form_record.url_path)

        assert result.id == sample_form_record.id
        assert result.url_path == sample_form_record.url_path
        assert result.display_name == sample_form_record.display_name
        assert result.draft_json == sample_form_record.draft_json
        assert result.published_json == sample_form_record.published_json

    def test_get_form_by_url_path_not_found(self, db):
        """Test get_form_by_url_path raises NoResultFound for non-existent form."""
        with pytest.raises(NoResultFound):
            get_form_by_url_path("non-existent-form")


class TestCreateOrUpdateForm:
    """Tests for create_or_update_form query."""

    def test_create_new_form(self, db):
        """Test create_or_update_form creates new form."""
        url_path = "new-test-form"
        display_name = "New Test Form"
        form_json = {"pages": [{"path": "/test", "title": "Test"}], "startPage": "/test"}

        result = create_or_update_form(url_path, display_name, form_json)

        assert result.url_path == url_path
        assert result.display_name == display_name
        assert result.draft_json == form_json
        assert result.published_json == {}
        assert result.created_at is not None
        assert result.updated_at is not None

        # Verify it was saved to database
        saved_form = db.session.query(FormDefinition).filter_by(url_path=url_path).first()
        assert saved_form is not None
        assert saved_form.url_path == url_path

    def test_update_existing_form(self, db, sample_form_record):
        """Test create_or_update_form updates existing form."""
        new_form_json = {"pages": [{"path": "/updated", "title": "Updated"}], "startPage": "/updated"}
        new_display_name = "Updated Form"

        result = create_or_update_form(sample_form_record.url_path, new_display_name, new_form_json)

        assert result.id == sample_form_record.id
        assert result.url_path == sample_form_record.url_path
        assert result.display_name == new_display_name
        assert result.draft_json == new_form_json
        assert result.published_json == sample_form_record.published_json  # Should remain unchanged

        # Verify database was updated
        db.session.refresh(sample_form_record)
        assert sample_form_record.draft_json == new_form_json
        assert sample_form_record.display_name == new_display_name


class TestPublishForm:
    """Tests for publish_form query."""

    def test_publish_form_success(self, db, sample_form_record):
        """Test publish_form copies draft to published."""
        original_published_at = sample_form_record.published_at

        result = publish_form(sample_form_record.url_path)

        assert result.id == sample_form_record.id
        assert result.url_path == sample_form_record.url_path
        assert result.published_json == sample_form_record.draft_json
        assert result.published_at is not None
        assert result.published_at != original_published_at

        # Verify database was updated
        db.session.refresh(sample_form_record)
        assert sample_form_record.published_json == sample_form_record.draft_json
        assert sample_form_record.published_at is not None

    def test_publish_form_not_found(self, db):
        """Test publish_form raises NoResultFound for non-existent form."""
        with pytest.raises(NoResultFound):
            publish_form("non-existent-form")

    def test_publish_form_no_draft(self, db):
        """Test publish_form raises ValueError when no draft exists."""
        # Create form with no draft_json
        form = FormDefinition(url_path="no-draft-form", draft_json=None, published_json={})
        db.session.add(form)
        db.session.commit()

        with pytest.raises(ValueError) as exc_info:
            publish_form("no-draft-form")
        assert "has no draft to publish" in str(exc_info.value)

    def test_publish_form_empty_draft(self, db):
        """Test publish_form raises ValueError when draft is empty dict."""
        # Create form with empty draft_json
        form = FormDefinition(url_path="empty-draft-form", draft_json={}, published_json={})
        db.session.add(form)
        db.session.commit()

        # Empty dict should be considered as "no draft"
        with pytest.raises(ValueError) as exc_info:
            publish_form("empty-draft-form")
        assert "has no draft to publish" in str(exc_info.value)

    @patch("pre_award.form_store.db.queries.datetime")
    def test_publish_form_sets_current_timestamp(self, mock_datetime, db, sample_form_record):
        """Test publish_form sets published_at to current timestamp."""
        mock_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now

        result = publish_form(sample_form_record.url_path)

        assert result.published_at == mock_now
        mock_datetime.now.assert_called_once()


class TestFormDefinitionModel:
    """Tests for FormDefinition model methods."""

    def test_as_dict_published_form(self, db, published_form_record):
        """Test as_dict method for published form (metadata only)."""
        result = published_form_record.as_dict()

        assert result["id"] == str(published_form_record.id)
        assert result["url_path"] == published_form_record.url_path
        assert result["display_name"] == published_form_record.display_name
        assert "draft_json" not in result
        assert "published_json" not in result
        assert result["is_published"] is True
        assert result["created_at"] is not None
        assert result["updated_at"] is not None
        assert result["published_at"] is not None

    def test_as_dict_unpublished_form(self, db, sample_form_record):
        """Test as_dict method for unpublished form (metadata only)."""
        result = sample_form_record.as_dict()

        assert result["id"] == str(sample_form_record.id)
        assert result["url_path"] == sample_form_record.url_path
        assert result["display_name"] == sample_form_record.display_name
        assert "draft_json" not in result
        assert "published_json" not in result
        assert result["is_published"] is False
        assert result["created_at"] is not None
        assert result["updated_at"] is not None
        assert result["published_at"] is None

    def test_as_dict_with_draft_json(self, db, sample_form_record):
        """Test as_dict_with_draft_json includes draft configuration."""
        result = sample_form_record.as_dict_with_draft_json()

        assert result["id"] == str(sample_form_record.id)
        assert result["url_path"] == sample_form_record.url_path
        assert result["display_name"] == sample_form_record.display_name
        assert result["draft_json"] == sample_form_record.draft_json
        assert "published_json" not in result
        assert result["is_published"] is False

    def test_as_dict_with_published_json(self, db, published_form_record):
        """Test as_dict_with_published_json includes published configuration."""
        result = published_form_record.as_dict_with_published_json()

        assert result["id"] == str(published_form_record.id)
        assert result["url_path"] == published_form_record.url_path
        assert result["display_name"] == published_form_record.display_name
        assert result["published_json"] == published_form_record.published_json
        assert "draft_json" not in result
        assert result["is_published"] is True

    def test_as_dict_handles_none_timestamps(self, db):
        """Test as_dict handles None timestamps gracefully."""
        form = FormDefinition(url_path="test-form", draft_json={"test": "data"}, published_json={})
        # Don't add to session to avoid auto-setting timestamps

        result = form.as_dict()

        assert result["created_at"] is None
        assert result["updated_at"] is None
        assert result["published_at"] is None
        assert result["is_published"] is False

    def test_is_published_logic(self, db):
        """Test is_published logic in as_dict method."""
        # Test with empty dict
        form1 = FormDefinition(url_path="form1", draft_json={}, published_json={})
        assert form1.as_dict()["is_published"] is False

        # Test with None
        form2 = FormDefinition(url_path="form2", draft_json={}, published_json=None)
        assert form2.as_dict()["is_published"] is False

        # Test with actual data
        form3 = FormDefinition(url_path="form3", draft_json={}, published_json={"test": "data"})
        assert form3.as_dict()["is_published"] is True
