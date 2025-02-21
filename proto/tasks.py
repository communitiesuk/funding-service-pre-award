import os
from contextlib import contextmanager
from datetime import datetime

from invoke import task
from sqlalchemy import func, select, text

from proto.common.data.models import Fund, ProtoReportingRound, TemplateSection
from proto.common.data.models.data_collection import ConditionCombination
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
            type=QuestionType.TEXT_INPUT,
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
            type=QuestionType.TEXT_INPUT,
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
            type=QuestionType.TEXTAREA,
            title="How much money should we give you?",
            hint=None,
            order=6,
            data_source=None,
            data_standard_id=None,
            template_section_id=template_sections_to_create["project-information"].id,
        ),
        "monitoring-project-money": TemplateQuestion(
            slug="monitoring-project-money",
            type=QuestionType.TEXTAREA,
            title="How much of the ((application.project_information.project_money)) allocated has been spent so far?",
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
            type=QuestionType.TEXT_INPUT,
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
    ]

    conditions_to_create = [
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
                preview=True,
                reporting_period_starts=datetime(2024, 1, 1),
                reporting_period_ends=datetime(2024, 6, 30),
                submission_period_starts=datetime(2024, 7, 1),
                submission_period_ends=datetime(2024, 9, 30),
                grant_id=fund.id,
            )
        )
        db.session.add(
            ProtoReportingRound(
                preview=True,
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

    db.session.commit()


@task
def seed_question_bank(c):
    from app import create_app

    with _env_var("FLASK_ENV", "development"):
        app = create_app()
        with app.app_context():
            insert_question_bank_data()
