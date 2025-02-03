from pre_award.apply.models.fund import Fund
from pre_award.apply.models.round import Round

default_hsra_round_fields = {
    "opens": "2022-09-01T00:00:01",
    "assessment_deadline": "2030-03-20T00:00:01",
    "contact_email": "test@example.com",
    "prospectus": "/hsra_rp_prospectus",
    "instructions": "Round specific instruction text",
    "privacy_notice": "http://privacy.com",
    "project_name_field_id": "",
    "feedback_link": "http://feedback.com",
    "application_guidance": "",
    "mark_as_complete_enabled": False,
    "is_expression_of_interest": False,
    "eligibility_config": {"has_eligibility": True},
}

default_hsra_fund_fields = {
    "id": "444",
    "name": "HSRA",
    "description": "test HSRA Fund",
    "short_name": "HSRA",
    "title": "High Street Rental Funds",
    "welsh_available": False,
    "funding_type": "COMPETITIVE",
}


def test_eligibility_result(apply_test_client, mocker, mock_login, templates_rendered):
    def mock_fund_and_round(short_name, round_id, title):
        mocker.patch(
            "pre_award.apply.helpers.get_fund_data_by_short_name",
            return_value=Fund.from_dict(default_hsra_fund_fields),
        )
        mocker.patch(
            "pre_award.apply.helpers.get_round_data_by_short_names",
            return_value=Round.from_dict(
                {
                    **default_hsra_round_fields,
                    "fund_id": "444",
                    "id": round_id,
                    "short_name": short_name,
                    "title": title,
                    "deadline": "2050-01-01T00:00:01",
                }
            ),
        )

    # Test eligibility result with redirect_to_eligible_round parameter
    mock_fund_and_round("RP", "hsra-rp", "Refurbishment Project")
    result = apply_test_client.get("/eligibility-result/hsra/vr?redirect_to_eligible_round=RP")
    assert result.status_code == 302
    assert result.location.endswith("/account/new?fund_id=444&round_id=hsra-rp")

    # Test eligibility result without redirect_to_eligible_round parameter
    mock_fund_and_round("VR", "hsra-vr", "Vacancy Register")
    result = apply_test_client.get("/eligibility-result/hsra/vr")
    assert result.status_code == 302
    assert result.location.endswith("/account/new?fund_id=444&round_id=hsra-vr")
