import json

import pytest
from fsd_utils import Decision, evaluate_response

from pre_award.fund_store.config.fund_loader_config.cof.eoi_r1_schema import (
    COF_PLANNING_PERMISSION_CAVEAT_EN,
    COF_PLANNING_PERMISSION_IF_NEEDED_CAVEAT_EN,
    COF_R3_EOI_SCHEMA_EN,
    COF_SECURE_MATCH_FUNDING_CAVEAT_EN,
)


def test_eoi_schema_throws_no_errors_with_all_forms():
    with open("tests/fund_store_tests/test_data/cof_eoi.json", "r") as f:
        forms = json.loads(f.read())
    result = evaluate_response(schema=COF_R3_EOI_SCHEMA_EN, forms=forms)

    assert result


@pytest.mark.parametrize(
    "question_key,supplied_answer,exp_decision,exp_caveats",
    [
        ("non-existant-question", "anything", Decision.PASS, []),
        (
            "uYiLsv",
            "not-yet-incorporated",
            Decision.PASS_WITH_CAVEATS,
            [
                "Incorporate your organisation: You must have incorporated your"
                " organisation by the time you submit a full application. If you remain"
                " unincorporated, your application will be ineligible."
            ],
        ),
        ("NcQSbU", True, Decision.FAIL, []),
        ("eEaDGz", False, Decision.FAIL, []),
        ("zurxox", False, Decision.FAIL, []),
        ("lLQmNb", False, Decision.FAIL, []),
        ("fBhSNc", False, Decision.FAIL, []),
        ("eOWKoO", False, Decision.FAIL, []),
        ("foQgiy", False, Decision.FAIL, []),
        (
            "XuAyrs",
            "Yes, a town, parish or community council",
            Decision.PASS_WITH_CAVEATS,
            [COF_R3_EOI_SCHEMA_EN["XuAyrs"][0]["caveat"]],
        ),
        (
            "XuAyrs",
            "Yes, another type of public authority",
            Decision.PASS_WITH_CAVEATS,
            [COF_R3_EOI_SCHEMA_EN["XuAyrs"][1]["caveat"]],
        ),
        (
            "BykoQQ",
            ["Not sure"],
            Decision.PASS_WITH_CAVEATS,
            [COF_R3_EOI_SCHEMA_EN["BykoQQ"][0]["caveat"]],
        ),
        (
            "oblxxv",
            False,
            Decision.PASS_WITH_CAVEATS,
            [COF_R3_EOI_SCHEMA_EN["oblxxv"][0]["caveat"]],
        ),
        (
            "kWRuac",
            "Not yet approached any funders",
            Decision.PASS_WITH_CAVEATS,
            [COF_SECURE_MATCH_FUNDING_CAVEAT_EN],
        ),
        (
            "kWRuac",
            "Approached some funders but not yet secured",
            Decision.PASS_WITH_CAVEATS,
            [COF_SECURE_MATCH_FUNDING_CAVEAT_EN],
        ),
        (
            "kWRuac",
            "Secured some match funding",
            Decision.PASS_WITH_CAVEATS,
            [COF_SECURE_MATCH_FUNDING_CAVEAT_EN],
        ),
        (
            "kWRuac",
            "Approached all funders but not yet secured",
            Decision.PASS_WITH_CAVEATS,
            [COF_SECURE_MATCH_FUNDING_CAVEAT_EN],
        ),
        (
            "yZxdeJ",
            True,
            Decision.PASS_WITH_CAVEATS,
            [COF_R3_EOI_SCHEMA_EN["yZxdeJ"][0]["caveat"]],
        ),
        (
            "UORyaF",
            "Not sure",
            Decision.PASS_WITH_CAVEATS,
            [COF_PLANNING_PERMISSION_IF_NEEDED_CAVEAT_EN],
        ),
        (
            "jICagT",
            "Not yet started",
            Decision.PASS_WITH_CAVEATS,
            [COF_PLANNING_PERMISSION_CAVEAT_EN],
        ),
        (
            "jICagT",
            "Early stage",
            Decision.PASS_WITH_CAVEATS,
            [COF_PLANNING_PERMISSION_CAVEAT_EN],
        ),
        ("fZAMFv", "2000001", Decision.FAIL, []),
    ],
)
def test_answer_and_result(question_key, supplied_answer, exp_decision, exp_caveats):
    # Construct a dummy form with the supplied question and answer
    forms = [
        {
            "name": "COF EOI Test question",
            "questions": [
                {
                    "question": "Test question",
                    "fields": [
                        {
                            "key": question_key,
                            "title": "test question",
                            "type": "test",
                            "answer": supplied_answer,
                        }
                    ],
                }
            ],
        },
    ]
    # evaluate a response
    result = evaluate_response(schema=COF_R3_EOI_SCHEMA_EN, forms=forms)

    assert result
    assert result["decision"] == exp_decision
    assert result["caveats"] == exp_caveats


@pytest.mark.parametrize("question_key", COF_R3_EOI_SCHEMA_EN.keys())
def test_answers_with_non_conditioned_values(question_key):
    # Construct a dummy form with the supplied question and answer
    forms = [
        {
            "name": "COF EOI Test question",
            "questions": [
                {
                    "question": "Test question",
                    "fields": [
                        {
                            "key": question_key,
                            "title": "test question",
                            "type": "test",
                            "answer": "123",
                        }
                    ],
                }
            ],
        },
    ]
    # evaluate a response
    result = evaluate_response(schema=COF_R3_EOI_SCHEMA_EN, forms=forms)

    assert result
    assert result["decision"] == Decision.PASS
    assert result["caveats"] == []
