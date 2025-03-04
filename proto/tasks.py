import os
from contextlib import contextmanager
from datetime import datetime

from invoke import task
from sqlalchemy import func, select, text

from proto.common.data.models import Fund, Organisation, ProtoReportingRound, TemplateSection
from proto.common.data.models.data_collection import ConditionCombination, DataStore, DataStoreEntry
from proto.common.data.models.question_bank import (
    DataStandard,
    QuestionType,
    TemplateQuestion,
    TemplateQuestionCondition,
    TemplateType,
    TemplateValidation,
)


@contextmanager
def _env_var(key, value):
    old_val = os.environ.get(key, "")
    os.environ[key] = value
    yield
    os.environ[key] = old_val


def insert_question_bank_data():
    from db import db

    local_council_data_store = DataStore(collection_name="Local councils")
    local_council_data_store.data.extend(
        [
            DataStoreEntry(value="E06000038", label="Reading Borough Council"),
            DataStoreEntry(value="E10000025", label="Oxford City Council"),
        ]
    )

    db.session.add(local_council_data_store)
    db.session.commit()

    data_standards_to_create = {
        "user.schema.json#properties/full_name": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/user.schema.json#properties/full_name",
            description="A person's name",
        ),
        "organisation.schema.json#properties/name": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/organisation.schema.json#properties/name",
            description="The organisation name",
        ),
        "organisation.schema.json#properties/type": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/organisation.schema.json#properties/type",
            description="The organisation type",
        ),
        "risk.schema.json#properties/risk_title": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/risk.schema.json#properties/risk_title",
            description="A short description of the risk",
        ),
        "risk.schema.json#properties/risk_description": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/risk.schema.json#properties/risk_description",
            description="The details of the risk",
        ),
        "risk.schema.json#properties/risk_category": DataStandard(
            slug="https://www.github.com/communitiesuk/funding-service-data-standards/schemas/risk.schema.json#properties/principal_risk_category",
            description="The primary categorisation of the risk",
        ),
    }
    for _, ds_instance in data_standards_to_create.items():
        ds_id = db.session.scalar(text("select id from data_standard where slug = :slug"), dict(slug=ds_instance.slug))
        if not ds_id:
            db.session.add(ds_instance)
        else:
            ds_instance.id = ds_id
            db.session.merge(ds_instance)
        db.session.flush()

    template_sections_to_create = {
        "project-information": TemplateSection(
            slug="project-information", title="Project Information", order=1, type=TemplateType.APPLICATION
        ),
        "organisation-information": TemplateSection(
            slug="organisation-information",
            title="Organisation Information",
            order=2,
            type=TemplateType.APPLICATION,
        ),
        "risk-information": TemplateSection(
            slug="risk-information",
            title="Risks",
            order=3,
            type=TemplateType.APPLICATION,
        ),
        "tea-licensing": TemplateSection(
            slug="tea-licensing",
            title="Tea licensing",
            order=0,
            type=TemplateType.APPLICATION,
        ),
        # Hack - possibly would de-dupe this if we were doing it for real
        "monitoring-risk-information": TemplateSection(
            slug="monitoring-risk-information",  # hack - maybe should be unique on slug+type
            title="Risks",
            order=1,
            type=TemplateType.REPORTING,
        ),
        "monitoring-project-information": TemplateSection(
            slug="monitoring-project-information",
            title="Project Information",
            order=2,
            type=TemplateType.REPORTING,
        ),
        "tea-statistics-r1": TemplateSection(
            slug="tea-statistics-r1",
            title="Tea statistics (R1)",
            order=-100,
            type=TemplateType.REPORTING,
        ),
        "tea-statistics-r2": TemplateSection(
            slug="tea-statistics-r2",
            title="Tea statistics (R2)",
            order=-99,
            type=TemplateType.REPORTING,
        ),
    }
    for ts_slug, ts_instance in template_sections_to_create.items():
        ts_id = db.session.execute(
            text("select id from template_section where slug = :slug"), dict(slug=ts_slug)
        ).scalar_one_or_none()
        if not ts_id:
            db.session.add(ts_instance)
        else:
            ts_instance.id = ts_id
            db.session.merge(ts_instance)
        db.session.flush()

    template_questions_to_create = {
        "cups-of-tea": TemplateQuestion(
            slug="cups-of-tea",
            type=QuestionType.NUMBER,
            title="How many cups of tea would you like funding for?",
            hint=(
                "We will give you permissions to serve this many cups of tea. "
                "You will not be allowed to serve more than this."
            ),
            order=1,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["tea-licensing"].id,
        ),
        "price-per-cup": TemplateQuestion(
            slug="price-per-cup",
            type=QuestionType.POUNDS_AND_PENCE,
            title="How much does it cost you to serve a cup of tea?",
            hint=None,
            order=2,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["tea-licensing"].id,
        ),
        "fraud-is-bad": TemplateQuestion(
            slug="fraud-is-bad",
            type=QuestionType.RADIOS,
            title="Are you trying to defraud the taxpayer?",
            hint="More than £5 per cup of tea is excessive.",
            order=3,
            data_source=[
                {"value": "good-boy", "label": "All of my costs are legitimate and strictly tea-related"},
                {"value": "bad-boy", "label": "I am trying to commit fraud"},
            ],
            data_standard_id=None,
            template_section_id=template_sections_to_create["tea-licensing"].id,
        ),
        "cups-served-r1": TemplateQuestion(
            slug="cups-served",
            type=QuestionType.NUMBER,
            title="How many cups of tea did you serve between ((reporting_round.reporting_period_starts)) and ((reporting_round.reporting_period_ends))?",  # noqa
            hint="You applied for funding to serve a total of ((application.tea_licensing.cups_of_tea)) cups of tea.",
            order=1,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["tea-statistics-r1"].id,
        ),
        "tea-money-spent-r1": TemplateQuestion(
            slug="tea-money-spent",
            type=QuestionType.POUNDS_AND_PENCE,
            title="How much did it cost you?",
            hint="We will pay you this much money. You applied for £(( int(application.tea_licensing.cups_of_tea * application.tea_licensing.price_per_cup) )) in funding, and have been allocated £((recipient.funding_allocated)).",  # noqa
            order=2,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["tea-statistics-r1"].id,
        ),
        "cups-served-r2": TemplateQuestion(
            slug="cups-served",
            type=QuestionType.NUMBER,
            title="How many cups of tea did you serve between ((reporting_round.reporting_period_starts)) and ((reporting_round.reporting_period_ends))?",  # noqa
            hint="You applied for funding to serve a total of ((application.tea_licensing.cups_of_tea)) cups of tea. You have received funding for ((reports[0].tea_statistics_r1.cups_served)) so far.",  # noqa
            order=1,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["tea-statistics-r2"].id,
        ),
        "tea-money-spent-r2": TemplateQuestion(
            slug="tea-money-spent",
            type=QuestionType.POUNDS_AND_PENCE,
            title="How much did it cost you?",
            hint="We will pay you this much money. You applied for £(( int(application.tea_licensing.cups_of_tea * application.tea_licensing.price_per_cup) )) in funding, and have been allocated £((recipient.funding_allocated)).",  # noqa
            order=2,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["tea-statistics-r2"].id,
        ),
        "project-name": TemplateQuestion(
            slug="project-name",
            type=QuestionType.TEXT_INPUT,
            title="What is the name of your project?",
            hint=None,
            order=1,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "project-size": TemplateQuestion(
            slug="project-size",
            type=QuestionType.NUMBER,
            title=(
                "How many people will work on ((this_collection.project_information.project_name or 'this project'))?"
            ),
            hint="Can be to the nearest 10",
            order=2,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "project-size-big": TemplateQuestion(
            slug="project-size-big",
            type=QuestionType.TEXT_INPUT,
            title="What's the make up of this team?",
            hint="eg. expected to be 1 head chef, 2 sous chefs, 10 waiters, 1 front of house",
            order=3,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "project-size-small": TemplateQuestion(
            slug="project-size-small",
            type=QuestionType.NUMBER,
            title="How many cups of tea do you expect to get through in a day?",
            hint=None,
            order=4,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "project-about": TemplateQuestion(
            slug="project-about",
            type=QuestionType.TEXTAREA,
            title="What is your project about?",
            hint="Give a brief summary of your project, including what you hope to achieve",
            order=5,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "project-money": TemplateQuestion(
            slug="project-money",
            type=QuestionType.NUMBER,
            title="How much money should we give you?",
            hint=None,
            order=6,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "project-local-council": TemplateQuestion(
            slug="project-local-council",
            type=QuestionType.LIST_AUTOCOMPLETE,
            title="When local council?",
            hint=None,
            order=7,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
            reference_data_source=local_council_data_store,
        ),
        "monitoring-project-money": TemplateQuestion(
            slug="monitoring-project-money",
            type=QuestionType.NUMBER,
            title="How much of the £((recipient.funding_allocated)) you've been given has been spent so far?",
            hint=None,
            order=1,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["monitoring-project-information"].id,
        ),
        "organisation-name": TemplateQuestion(
            slug="organisation-name",
            type=QuestionType.TEXT_INPUT,
            title="What is the name of your organisation?",
            hint=None,
            order=1,
            data_source=None,
            data_standard_id=data_standards_to_create["organisation.schema.json#properties/name"].id,
            template_section_id=template_sections_to_create["organisation-information"].id,
        ),
        "organisation-kind": TemplateQuestion(
            slug="organisation-kind",
            type=QuestionType.RADIOS,
            title="What kind of organisation are you in?",
            hint=None,
            order=2,
            data_source=[
                {"value": "charity", "label": "Charity"},
                {"value": "local-authority", "label": "Local Authority"},
                {"value": "limited-company", "label": "Limited company"},
                {"value": "other", "label": "Other"},
            ],
            data_standard_id=data_standards_to_create["organisation.schema.json#properties/type"].id,
            template_section_id=template_sections_to_create["organisation-information"].id,
        ),
        "local-authority-name": TemplateQuestion(
            slug="local-authority-name",
            type=QuestionType.TEXT_INPUT,
            title="What is the name of your local authority?",
            hint=None,
            order=3,
            data_source=[
                {"value": "cornwall-ua", "label": "Cornwall Unitary Authority"},
                {"value": "newport-cc", "label": "Newport City Council"},
                {"value": "torfaen-bc", "label": "Torfaen Borough Authority"},
            ],
            data_standard_id=None,
            template_section_id=template_sections_to_create["organisation-information"].id,
            condition_combination_type=ConditionCombination.AND,
        ),
        "organisation-type-other": TemplateQuestion(
            slug="organisation-type-other",
            type=QuestionType.TEXT_INPUT,
            title="What type of organisation are you in (other)?",
            hint=None,
            order=4,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["organisation-information"].id,
            condition_combination_type=ConditionCombination.AND,
        ),
        "company-registration-number": TemplateQuestion(
            slug="company-registration-number",
            type=QuestionType.TEXT_INPUT,
            title="What is your company registration number?",
            hint=None,
            order=5,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["organisation-information"].id,
            condition_combination_type=ConditionCombination.OR,
        ),
        "organisation-owner": TemplateQuestion(
            slug="organisation-owner",
            type=QuestionType.TEXT_INPUT,
            title="Who is your ((this_collection.organisation_information.organisation_kind or 'organisation'))'s owner?",  # noqa
            hint=None,
            order=6,
            data_source=None,
            data_standard_id=data_standards_to_create["user.schema.json#properties/full_name"].id,
            template_section_id=template_sections_to_create["organisation-information"].id,
        ),
        "organisation-annual-turnover": TemplateQuestion(
            slug="organisation-annual-turnover",
            type=QuestionType.NUMBER,
            title="What is your organisation's annual turnover?",
            hint="To the nearest £10k",
            order=7,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["organisation-information"].id,
            condition_combination_type=ConditionCombination.AND,
        ),
        "risk-title": TemplateQuestion(
            slug="risk-title",
            type=QuestionType.TEXT_INPUT,
            title="What is the risk to your project?",
            hint="Summarise the risk to delivering good value for money for ((grant.name_json.en)) in a single sentence",  # noqa
            order=1,
            data_source=None,
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_title"].id,
            template_section_id=template_sections_to_create["risk-information"].id,
        ),
        "risk-description": TemplateQuestion(
            slug="risk-description",
            type=QuestionType.TEXTAREA,
            title="Tell us more about the risk to your project.",
            hint="""<p class="govuk-hint">
            You should cover:
            <ul class="govuk-list govuk-list--bullet govuk-hint">
            <li>What could go wrong?</li>
            <li>What could cause things to go wrong?</li>
            <li>What would the outcome be if it did go wrong?</li>
            </ul>
            </p>""",
            order=2,
            data_source=None,
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_description"].id,
            template_section_id=template_sections_to_create["risk-information"].id,
        ),
        "risk-category": TemplateQuestion(
            slug="risk-category",
            type=QuestionType.RADIOS,
            title="What is the main category for this risk?",
            hint=None,
            order=3,
            data_source=[
                {"value": val, "label": val}
                for val in [
                    "Arms length bodies",
                    "Commercial",
                    "Financial",
                    "Governance",
                    "Information and data",
                    "Legal",
                    "Local Government delivery",
                    "People",
                    "Project delivery",
                    "Resilience",
                    "Security",
                    "Strategy",
                    "Systems and infrastructure",
                ]
            ],
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_category"].id,
            template_section_id=template_sections_to_create["risk-information"].id,
        ),
        "monitoring-risk-title": TemplateQuestion(
            slug="risk-title",
            type=QuestionType.TEXT_INPUT,
            title="What is the risk to your project?",
            hint="Summarise the risk in a single sentence",
            order=1,
            data_source=None,
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_title"].id,
            template_section_id=template_sections_to_create["monitoring-risk-information"].id,
        ),
        "monitoring-risk-description": TemplateQuestion(
            slug="risk-description",
            type=QuestionType.TEXTAREA,
            title="Tell us more about the risk to your project.",
            hint="""<p class="govuk-hint">
            You should cover:
            <ul class="govuk-list govuk-list--bullet govuk-hint">
            <li>What could go wrong?</li>
            <li>What could cause things to go wrong></li>
            <li>What would the outcome be if it did go wrong?</li>
            </ul>
            </p>""",
            order=2,
            data_source=None,
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_description"].id,
            template_section_id=template_sections_to_create["monitoring-risk-information"].id,
        ),
        "monitoring-risk-category": TemplateQuestion(
            slug="risk-category",
            type=QuestionType.RADIOS,
            title="What is the main category for this risk?",
            hint=None,
            order=3,
            data_source=[
                {"value": val, "label": val}
                for val in [
                    "Arms length bodies",
                    "Commercial",
                    "Financial",
                    "Governance",
                    "Information and data",
                    "Legal",
                    "Local Government delivery",
                    "People",
                    "Project delivery",
                    "Resilience",
                    "Security",
                    "Strategy",
                    "Systems and infrastructure",
                ]
            ],
            data_standard_id=data_standards_to_create["risk.schema.json#properties/risk_category"].id,
            template_section_id=template_sections_to_create["monitoring-risk-information"].id,
        ),
    }
    for _, tq_instance in template_questions_to_create.items():
        tq_id = db.session.execute(
            text("select id from template_question where template_section_id = :template_section_id and slug = :slug"),
            dict(template_section_id=tq_instance.template_section_id, slug=tq_instance.slug),
        ).scalar_one_or_none()
        if not tq_id:
            db.session.add(tq_instance)
        else:
            tq_instance.id = tq_id
            db.session.merge(tq_instance)
        db.session.flush()
    db.session.commit()

    validations_to_create = [
        TemplateValidation(
            question_id=template_questions_to_create["project-size"].id,
            expression="int(answer) <= 30",
            message="The number of people working must be 30 or less",
        ),
        TemplateValidation(
            question_id=template_questions_to_create["project-size"].id,
            expression="int(answer) >= 1",
            message="The number of people working must be 1 or more",
        ),
        TemplateValidation(
            question_id=template_questions_to_create["cups-of-tea"].id,
            expression="0 < answer <= 1000",
            message="Tea licences are only available for 0-1000 cups of tea",
        ),
        TemplateValidation(
            question_id=template_questions_to_create["price-per-cup"].id,
            expression="0 < answer <= 10",
            message="We will only fund tea that can be served for £10 a cup or cheaper",
        ),
        TemplateValidation(
            question_id=template_questions_to_create["fraud-is-bad"].id,
            expression="answer == 'good-boy'",
            message="Try again",
        ),
        TemplateValidation(
            question_id=template_questions_to_create["cups-served-r1"].id,
            expression="answer <= application.tea_licensing.cups_of_tea",
            message="Your license only allows you to serve ((application.tea_licensing.cups_of_tea)) cups of tea",
        ),
        TemplateValidation(
            question_id=template_questions_to_create["tea-money-spent-r1"].id,
            expression="answer <= (application.tea_licensing.cups_of_tea * application.tea_licensing.price_per_cup)",
            message=(
                "You only applied for "
                "£((application.tea_licensing.cups_of_tea * application.tea_licensing.price_per_cup)) in funding, "
                "based on ((application.tea_licensing.cups_of_tea)) cups of tea "
                "at £((application.tea_licensing.price_per_cup)) per cup."
            ),
        ),
        TemplateValidation(
            question_id=template_questions_to_create["tea-money-spent-r1"].id,
            expression="answer <= (recipient.funding_allocated)",
            message=(
                "The funding team allocated you £((recipient.funding_allocated)). You will need to speak "
                "to them if this is incorrect."
            ),
        ),
        TemplateValidation(
            question_id=template_questions_to_create["cups-served-r2"].id,
            expression="(answer + reports[0].tea_statistics_r1.cups_served) <= application.tea_licensing.cups_of_tea",
            message=(
                "Your license only allows you to serve ((application.tea_licensing.cups_of_tea)) cups of tea. "
                "You served ((reports[0].tea_statistics_r1.cups_served)) cups last period, so can only report "
                "up to ((application.tea_licensing.cups_of_tea - reports[0].tea_statistics_r1.cups_served)) more."
            ),
        ),
        TemplateValidation(
            question_id=template_questions_to_create["tea-money-spent-r2"].id,
            expression=("answer <= (application.tea_licensing.cups_of_tea * application.tea_licensing.price_per_cup)"),
            message=(
                "You only applied for "
                "£((application.tea_licensing.cups_of_tea * application.tea_licensing.price_per_cup)) in funding, "
                "based on ((application.tea_licensing.cups_of_tea)) cups of tea "
                "at £((application.tea_licensing.price_per_cup)) per cup."
            ),
        ),
        TemplateValidation(
            question_id=template_questions_to_create["tea-money-spent-r2"].id,
            expression="(answer + reports[0].tea_statistics_r1.tea_money_spent) <= (recipient.funding_allocated)",
            message=(
                "The funding team allocated you £((recipient.funding_allocated)). "
                "You claimed £((reports[0].tea_statistics_r1.tea_money_spent)) in your last reporting period. "
                "You can only claim another £((recipient.funding_allocated - reports[0].tea_statistics_r1.tea_money_spent)). "  # noqa
                "You will need to speak to the fund team if this is incorrect."
            ),
        ),
    ]

    conditions_to_create = [
        TemplateQuestionCondition(
            question_id=template_questions_to_create["fraud-is-bad"].id,
            depends_on_question_id=template_questions_to_create["price-per-cup"].id,
            criteria={},
            expression="this_collection.tea_licensing.price_per_cup >= 5",
        ),
        TemplateQuestionCondition(
            question_id=template_questions_to_create["local-authority-name"].id,
            depends_on_question_id=template_questions_to_create["organisation-kind"].id,
            criteria={
                "operator": "EQUALS",
                "value_type": "QUESTION_VALUE",
                "value": "local-authority",
            },
            expression='answer == "local-authority"',
        ),
        TemplateQuestionCondition(
            question_id=template_questions_to_create["company-registration-number"].id,
            depends_on_question_id=template_questions_to_create["organisation-kind"].id,
            criteria={
                "operator": "EQUALS",
                "value_type": "QUESTION_VALUE",
                "value": "limited-company",
            },
            expression='answer == "limited-company"',
        ),
        TemplateQuestionCondition(
            question_id=template_questions_to_create["company-registration-number"].id,
            depends_on_question_id=template_questions_to_create["organisation-kind"].id,
            criteria={
                "operator": "EQUALS",
                "value_type": "QUESTION_VALUE",
                "value": "charity",
            },
            expression='answer == "charity"',
        ),
        TemplateQuestionCondition(
            question_id=template_questions_to_create["organisation-type-other"].id,
            depends_on_question_id=template_questions_to_create["organisation-kind"].id,
            criteria={
                "operator": "EQUALS",
                "value_type": "QUESTION_VALUE",
                "value": "other",
            },
            expression='answer == "other"',
        ),
        TemplateQuestionCondition(
            question_id=template_questions_to_create["project-size-big"].id,
            depends_on_question_id=template_questions_to_create["project-size"].id,
            criteria={
                "operator": "GREATERTHANEQUALS",
                "value_type": "QUESTION_VALUE",
                "value": "20",
            },
            expression="int(answer) >= 20",
        ),
        TemplateQuestionCondition(
            question_id=template_questions_to_create["project-size-small"].id,
            depends_on_question_id=template_questions_to_create["project-size"].id,
            criteria={
                "operator": "LESSTHAN",
                "value_type": "QUESTION_VALUE",
                "value": "20",
            },
            expression="int(answer) < 20",
        ),
        TemplateQuestionCondition(
            question_id=template_questions_to_create["organisation-annual-turnover"].id,
            depends_on_question_id=template_questions_to_create["project-size"].id,
            criteria={
                "operator": "GREATERTHANEQUALS",
                "value_type": "QUESTION_VALUE",
                "value": "30",
            },
            expression="int(answer) >= 30",
        ),
    ]

    db.session.execute(text("delete from template_question_condition"))
    for c_instance in conditions_to_create:
        db.session.add(c_instance)
        db.session.flush()

    # And do some other stuff to make my life easier sorry steven+sarah+marc+gideon+everyone else 🙇‍♂️
    funds = db.session.scalars(
        select(Fund).outerjoin(ProtoReportingRound).group_by(Fund.id).having(func.count(ProtoReportingRound.id) == 0)
    ).all()
    for fund in funds:
        db.session.add(
            ProtoReportingRound(
                preview=False,
                reporting_period_starts=datetime(2024, 1, 1),
                reporting_period_ends=datetime(2024, 6, 30),
                submission_period_starts=datetime(2024, 7, 1),
                submission_period_ends=datetime(2024, 9, 30),
                grant_id=fund.id,
            )
        )
        db.session.add(
            ProtoReportingRound(
                preview=False,
                reporting_period_starts=datetime(2024, 7, 1),
                reporting_period_ends=datetime(2025, 12, 31),
                submission_period_starts=datetime(2025, 1, 1),
                submission_period_ends=datetime(2025, 3, 31),
                grant_id=fund.id,
            )
        )
        db.session.flush()

    db.session.execute(text("delete from template_validation"))
    for validation_instance in validations_to_create:
        db.session.add(validation_instance)
        db.session.flush()
    db.session.commit()

    organisations_to_create = [
        Organisation(name="MHCLG", domain="communities.gov.uk"),
        Organisation(name="Bolton Council", domain="bolton.gov.uk"),
    ]
    for org_instance in organisations_to_create:
        org_id = db.session.scalar(text("select id from organisation where name = :name"), {"name": org_instance.name})
        if not org_id:
            db.session.add(org_instance)
        else:
            org_instance.id = org_id
            db.session.merge(org_instance)
        db.session.flush()

    db.session.commit()


@task
def seed_question_bank(c):
    from app import create_app

    with _env_var("FLASK_ENV", "development"):
        app = create_app()
        with app.app_context():
            insert_question_bank_data()
