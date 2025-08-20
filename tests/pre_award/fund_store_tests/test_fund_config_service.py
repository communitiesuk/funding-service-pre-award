"""
Tests for fund config service
"""

from unittest.mock import patch

import pytest

from pre_award.fund_store.services.save_fund_configuration import process_fund_config


@pytest.fixture
def sample_converted_config():
    """Sample converted fund config for testing"""
    return {
        "short_name": "TEST",
        "id": "test-fund-id",
        "rounds": {
            "r1": {
                "id": "test-round-id",
                "fund_id": "test-fund-id",
                "short_name": "r1",
                "base_path": 1001,
                "sections_config": [],
            }
        },
    }


def test_process_fund_config_success(sample_converted_config):
    """Test successful fund config processing"""
    with (
        patch("pre_award.fund_store.services.save_fund_configuration.insert_fund_data") as mock_insert_fund,
        patch("pre_award.fund_store.services.save_fund_configuration.upsert_round_data") as mock_upsert_round,
        patch("pre_award.fund_store.services.save_fund_configuration.insert_base_sections") as mock_insert_base,
        patch(
            "pre_award.fund_store.services.save_fund_configuration.insert_or_update_application_sections"
        ) as mock_insert_app,
        patch("pre_award.fund_store.services.save_fund_configuration.db.session.commit") as mock_commit,
    ):
        result = process_fund_config(sample_converted_config)

        assert result["success"] is True
        assert "Successfully processed fund configuration for TEST" == result["message"]

        # Verify all database operations were called
        mock_insert_fund.assert_called_once_with(sample_converted_config, commit=False)
        mock_upsert_round.assert_called_once_with(
            [
                {
                    "id": "test-round-id",
                    "fund_id": "test-fund-id",
                    "short_name": "r1",
                    "base_path": 1001,
                    "sections_config": [],
                }
            ],
            commit=False,
        )
        mock_insert_base.assert_called_once_with("1001.1", "1001.2", "test-round-id")
        mock_insert_app.assert_called_once_with("test-round-id", [])
        mock_commit.assert_called_once()


def test_process_fund_config_handles_errors(app, sample_converted_config):
    """Test error handling and rollback"""
    with app.app_context():
        with (
            patch(
                "pre_award.fund_store.services.save_fund_configuration.insert_fund_data",
                side_effect=Exception("Database connection failed"),
            ) as mock_insert,
            patch("pre_award.fund_store.services.save_fund_configuration.db.session.rollback") as mock_rollback,
        ):
            result = process_fund_config(sample_converted_config)

            assert result["success"] is False
            assert "Database connection failed" in result["message"]
            mock_insert.assert_called_once_with(sample_converted_config, commit=False)
            mock_rollback.assert_called_once()
