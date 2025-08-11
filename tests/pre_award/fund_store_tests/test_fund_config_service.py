"""
Tests for fund config service
"""

from unittest.mock import patch

from pre_award.fund_store.services.fund_config_service import process_fund_config


def test_process_fund_config_adds_defaults():
    """Test that missing organisation fields get default values"""
    config = {
        "short_name": "TEST",
        "rounds": {"r1": {"id": "test-id", "base_path": "test.path", "sections_config": {}}},
    }

    with (
        patch("pre_award.fund_store.services.fund_config_service.insert_fund_data"),
        patch("pre_award.fund_store.services.fund_config_service.upsert_round_data"),
        patch("pre_award.fund_store.services.fund_config_service.insert_base_sections"),
        patch("pre_award.fund_store.services.fund_config_service.insert_or_update_application_sections"),
        patch("pre_award.fund_store.services.fund_config_service.db.session.commit"),
    ):
        result = process_fund_config(config)

        assert result["success"] is True
        assert config["owner_organisation_name"] == ""
        assert config["owner_organisation_shortname"] == ""
        assert config["owner_organisation_logo_uri"] == ""


def test_process_fund_config_preserves_existing_values():
    """Test that existing organisation values are preserved"""
    config = {
        "short_name": "TEST",
        "owner_organisation_name": "Real Org",
        "rounds": {"r1": {"id": "test-id", "base_path": "test.path", "sections_config": {}}},
    }

    with (
        patch("pre_award.fund_store.services.fund_config_service.insert_fund_data"),
        patch("pre_award.fund_store.services.fund_config_service.upsert_round_data"),
        patch("pre_award.fund_store.services.fund_config_service.insert_base_sections"),
        patch("pre_award.fund_store.services.fund_config_service.insert_or_update_application_sections"),
        patch("pre_award.fund_store.services.fund_config_service.db.session.commit"),
    ):
        result = process_fund_config(config)

        assert result["success"] is True
        assert config["owner_organisation_name"] == "Real Org"


def test_process_fund_config_handles_errors():
    """Test error handling and rollback"""
    config = {
        "short_name": "TEST",
        "rounds": {"r1": {"id": "test-id", "base_path": "test.path", "sections_config": {}}},
    }

    with (
        patch("pre_award.fund_store.services.fund_config_service.insert_fund_data", side_effect=Exception("DB Error")),
        patch("pre_award.fund_store.services.fund_config_service.db.session.rollback") as mock_rollback,
    ):
        result = process_fund_config(config)

        assert result["success"] is False
        assert "DB Error" in result["message"]
        mock_rollback.assert_called_once()
