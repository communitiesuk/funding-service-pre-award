from collections import defaultdict

import pytest

from pre_award.assessment_store.api.routes._helpers import transform_to_assessor_task_list_metadata

COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_W3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"


@pytest.mark.skip(reason="used for tdd only")
def test_transform_to_assessor_task_list_metadata():
    SCORE_MAP = {
        "benefits": 1,
        "engagement": 2,
        "community-benefits": 5,
    }

    COMMENT_MAP = defaultdict(lambda: False)
    COMMENT_MAP["funding_breakdown"] = True

    sections, critera = transform_to_assessor_task_list_metadata(
        COF_FUND_ID,
        COF_ROUND_2_ID,
        SCORE_MAP,
        COMMENT_MAP,
    )

    assert sections == [
        {
            "name": "Unscored",
            "sub_criterias": [
                {"name": "Organisation information", "id": "org_info"},
                {"name": "Applicant information", "id": "applicant_info"},
                {"name": "Project information", "id": "project_info"},
                {"name": "Asset information", "id": "asset_info"},
                {"name": "Business plan", "id": "business_plan"},
            ],
        },
        {
            "name": "Declarations",
            "sub_criterias": [
                {"name": "Declarations", "id": "declarations"},
                {
                    "name": "Subsidy control and state aid",
                    "id": "subsidy_control_and_state_aid",
                },
            ],
        },
    ]

    assert critera == [
        {
            "name": "Strategic case",
            "total_criteria_score": 3,
            "number_of_scored_sub_criteria": 15,
            "weighting": 0.3,
            "sub_criterias": [
                {
                    "name": "Benefits",
                    "id": "benefits",
                    "score": 1,
                    "theme_count": 2,
                    "status": "COMPLETED",
                },
                {
                    "name": "Engagement",
                    "id": "engagement",
                    "score": 2,
                    "theme_count": 2,
                    "status": "COMPLETED",
                },
                {
                    "name": "Environmental Sustainability",
                    "id": "environmental_sustainability",
                    "score": None,
                    "theme_count": 1,
                    "status": "NOT_STARTED",
                },
            ],
        },
        {
            "name": "Management case",
            "total_criteria_score": 0,
            "number_of_scored_sub_criteria": 20,
            "weighting": 0.3,
            "sub_criterias": [
                {
                    "name": "Funding breakdown",
                    "id": "funding_breakdown",
                    "score": None,
                    "theme_count": 1,
                    "status": "IN_PROGRESS",
                },
                {
                    "name": "Financial and risk forecasts",
                    "id": "financial_and_risk_forecasts",
                    "score": None,
                    "theme_count": 3,
                    "status": "NOT_STARTED",
                },
                {
                    "name": "Skills and resources",
                    "id": "skills_and_resources",
                    "score": None,
                    "theme_count": 3,
                    "status": "NOT_STARTED",
                },
                {
                    "name": "Representation, inclusiveness and integration",
                    "id": "representation_inclusiveness_and_integration",
                    "score": None,
                    "theme_count": 2,
                    "status": "NOT_STARTED",
                },
            ],
        },
        {
            "name": "Potential to deliver community benefit",
            "total_criteria_score": 5,
            "number_of_scored_sub_criteria": 10,
            "weighting": 0.3,
            "sub_criterias": [
                {
                    "name": "How the community benefits\t",
                    "id": "community-benefits",
                    "score": 5,
                    "theme_count": 1,
                    "status": "COMPLETED",
                },
                {
                    "name": "How the asset will be inclusive",
                    "id": "how-the-asset-will-be-inclusive",
                    "score": None,
                    "theme_count": 1,
                    "status": "NOT_STARTED",
                },
            ],
        },
        {
            "name": "Added value of the community asset",
            "total_criteria_score": 0,
            "number_of_scored_sub_criteria": 5,
            "weighting": 0.1,
            "sub_criterias": [
                {
                    "name": "Value to the community",
                    "id": "value-to-the-community",
                    "score": None,
                    "theme_count": 1,
                    "status": "NOT_STARTED",
                }
            ],
        },
    ]
