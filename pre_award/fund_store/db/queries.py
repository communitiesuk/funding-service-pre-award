import uuid
from datetime import datetime
from typing import List

from sqlalchemy import bindparam, exc, func, insert, select, text, update
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.sql import expression
from sqlalchemy_utils import Ltree
from sqlalchemy_utils.types.ltree import LQUERY

from data.models import Fund, Round
from pre_award.db import db
from pre_award.fund_store.db.models.event import Event
from pre_award.fund_store.db.models.form_name import FormName
from pre_award.fund_store.db.models.section import AssessmentField, Section, SectionField


def get_all_funds() -> List[Fund]:
    funds = db.session.scalars(select(Fund)).all()
    return funds


def get_fund_by_id(
    fund_id: str,
) -> Fund:
    fund = db.session.scalars(select(Fund).filter(Fund.id == fund_id)).one()
    return fund


def get_fund_short_name(fund_id: str) -> str:
    fund = get_fund_by_id(fund_id)
    return fund.short_name if fund else "N/A"


def get_fund_by_short_name(
    fund_short_name: str,
) -> Fund:
    fund = db.session.scalar(select(Fund).filter(func.lower(Fund.short_name) == func.lower(fund_short_name)))
    return fund


def get_round_by_id(
    fund_id: str,
    round_id: str,
) -> Round:
    round = db.session.scalars(select(Round).filter(Round.id == round_id).filter(Round.fund_id == fund_id)).one()
    return round


def get_rounds_for_fund_by_id(
    fund_id: str,
) -> List[Round]:
    rounds = db.session.scalars(select(Round).filter(Round.fund_id == fund_id)).all()
    return rounds


def get_round_by_short_name(
    fund_short_name: str,
    round_short_name: str,
) -> Round:
    round = db.session.scalar(
        select(Round)
        .filter(func.lower(Round.short_name) == func.lower(round_short_name))
        .join(Fund)
        .filter(func.lower(Fund.short_name) == func.lower(fund_short_name))
    )
    return round


def get_rounds_for_fund_by_short_name(
    fund_short_name,
):
    rounds = db.session.scalars(
        select(Round).join(Fund).filter(func.lower(Fund.short_name) == func.lower(fund_short_name))
    ).all()
    return rounds


def get_sections_for_round(round_id) -> List[Section]:
    return db.session.scalars(select(Section).filter(Section.round_id == round_id).order_by(Section.path)).all()


def get_application_sections_for_round(
    fund_id,
    round_id,
) -> List[Section]:
    application_level = db.session.scalar(
        select(Section)
        .filter(Section.round_id == round_id)
        .filter(text("section.title_json->>'en' = 'Application'"))
        .join(Round)
        .filter(Round.fund_id == fund_id)
    )
    if not application_level:
        return None

    query = f"{application_level.path}.*{{1}}"
    lquery = expression.cast(query, LQUERY)
    application_sections = db.session.scalars(
        select(Section).filter(Section.path.lquery(lquery)).order_by(Section.path)
    ).all()

    return application_sections


def get_assessment_sections_for_round(
    fund_id,
    round_id,
    language,
) -> List[Section]:
    assessment_level = db.session.scalar(
        select(Section)
        .filter(Section.round_id == round_id)
        .filter(text("section.title_json->>'en' = 'Assessment'"))
        .join(Round)
        .filter(Round.fund_id == fund_id)
    )
    if not assessment_level:
        return None

    query = f"{assessment_level.path}.*{'{1}'}"
    lquery = expression.cast(query, LQUERY)
    # select(Section).join(Translation, onclause=(Section.title_content_id ==
    #  Translation.content_id) and (Translation.language == 'en'),
    #  isouter=True)
    # .filter(Section.id == 12)
    assessment_sections = db.session.scalars(
        select(Section)
        # .join
        # (
        #     Translation,
        #     onclause=and_((Translation.language == language),
        # (Section.title_content_id == Translation.content_id)),
        #     isouter=True
        # )
        # select (Section).filter(Section.path.lquery(lquery))
        # select(Section).join(Translation, onclause=f"section.title_content_id
        #  = translation.content_id and translation.language='{language}'",
        # isouter=True).filter(Section.path.lquery(lquery))
        .filter(Section.path.lquery(lquery))
        .order_by(Section.path)
    ).all()

    return assessment_sections


def create_event(
    type: str,
    activation_date: datetime,
    round_id: str = None,
    processed: datetime = None,
) -> Event:
    event = Event(
        type=type,
        activation_date=activation_date,
        round_id=round_id,
        processed=processed,
    )
    try:
        db.session.add(event)
        db.session.commit()
        db.session.refresh(event)
    except exc.IntegrityError:
        db.session.rollback()
        return None

    return event


def get_events(
    round_id: str = None,
    type: str = None,
    only_unprocessed: bool = False,
) -> List[Event]:
    query = select(Event)
    if round_id:
        query = query.filter(Event.round_id == round_id)

    if type:
        query = query.filter(Event.type == type)

    if only_unprocessed:
        query = query.filter(Event.processed != None)  # noqa

    events = db.session.scalars(query).all()
    return events


def get_event(round_id: str, event_id: str) -> Event:
    query = select(Event).filter(Event.id == event_id, Event.round_id == round_id)
    event = db.session.scalar(query)
    return event


def set_event_to_processed(event_id: str, processed: bool) -> Event:
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return None
    event.processed = datetime.now() if processed else None
    db.session.commit()
    return event


def upsert_fields(fields: list):
    stmt = (
        (
            postgres_insert(AssessmentField).values(
                id=bindparam("id"),
                title=bindparam("title"),
                field_type=bindparam("field_type"),
                display_type=bindparam("display_type"),
            )
        )
        .on_conflict_do_nothing(index_elements=[AssessmentField.id])
        .returning(AssessmentField.id)
    )

    update_params = [
        {
            "id": item["form_json_id"],
            "title": item["title"],
            "field_type": item["type"],
            "display_type": item["presentation_type"],
        }
        for item in fields
    ]

    result = db.session.execute(stmt, update_params)
    inserted_field_ids = [row.id for row in result]
    return inserted_field_ids


def insert_sections(sections):
    for section in sections:
        db.session.add(section)
    db.session.commit()


def insert_fund_data(fund_config, commit: bool = True):
    stmt = (
        (
            postgres_insert(Fund).values(
                id=bindparam("id"),
                name_json=bindparam("name_json"),
                title_json=bindparam("title_json"),
                short_name=bindparam("short_name"),
                description_json=bindparam("description_json"),
                welsh_available=bindparam("welsh_available"),
                owner_organisation_name=bindparam("owner_organisation_name"),
                owner_organisation_shortname=bindparam("owner_organisation_shortname"),
                owner_organisation_logo_uri=bindparam("owner_organisation_logo_uri"),
                ggis_scheme_reference_number=bindparam("ggis_scheme_reference_number"),
                funding_type=bindparam("funding_type"),
            )
        )
        .on_conflict_do_update(
            index_elements=[Fund.id],
            set_={
                "name_json": bindparam("name_json"),
                "title_json": bindparam("title_json"),
                "short_name": bindparam("short_name"),
                "description_json": bindparam("description_json"),
                "welsh_available": bindparam("welsh_available"),
                "owner_organisation_name": bindparam("owner_organisation_name"),
                "owner_organisation_shortname": bindparam("owner_organisation_shortname"),
                "owner_organisation_logo_uri": bindparam("owner_organisation_logo_uri"),
                "ggis_scheme_reference_number": bindparam("ggis_scheme_reference_number"),
                "funding_type": bindparam("funding_type"),
            },
        )
        .returning(Fund.id)
    )

    update_params = {
        "id": fund_config["id"],
        "name_json": fund_config["name_json"],
        "title_json": fund_config["title_json"],
        "short_name": fund_config["short_name"],
        "description_json": fund_config["description_json"],
        "welsh_available": fund_config["welsh_available"],
        "owner_organisation_name": fund_config["owner_organisation_name"],
        "owner_organisation_shortname": fund_config["owner_organisation_shortname"],
        "owner_organisation_logo_uri": fund_config["owner_organisation_logo_uri"],
        "ggis_scheme_reference_number": fund_config.get("ggis_scheme_reference_number"),
        "funding_type": fund_config["funding_type"],
    }

    result = db.session.execute(stmt, update_params)
    inserted_fund_ids = [row.id for row in result]

    print(f"Prepared fund for insert: '{inserted_fund_ids}'.")
    if commit:
        db.session.commit()
        print("DB changes committed")
    return inserted_fund_ids


def upsert_round_data(round_configs, commit: bool = True):
    # Create dictionary to store updated records
    updated_rounds = {}

    for round_config in round_configs:
        # Check if record exist
        round_record = Round.query.filter_by(id=round_config["id"]).first()

        if round_record is not None:
            # Update existing round record
            round_record.title_json = round_config["title_json"]
            round_record.short_name = round_config["short_name"]
            round_record.opens = round_config["opens"]
            round_record.assessment_start = round_config["assessment_start"]
            round_record.deadline = round_config["deadline"]
            round_record.application_reminder_sent = round_config["application_reminder_sent"]
            round_record.reminder_date = round_config["reminder_date"]
            round_record.fund_id = round_config["fund_id"]
            round_record.assessment_deadline = round_config["assessment_deadline"]
            round_record.prospectus = round_config["prospectus"]
            round_record.privacy_notice = round_config["privacy_notice"]
            round_record.contact_email = round_config["contact_email"]
            round_record.instructions_json = round_config["instructions_json"]
            round_record.project_name_field_id = round_config["project_name_field_id"]
            round_record.feedback_link = round_config["feedback_link"]
            round_record.application_guidance_json = round_config["application_guidance_json"]
            round_record.guidance_url = round_config["guidance_url"]
            round_record.all_uploaded_documents_section_available = round_config[
                "all_uploaded_documents_section_available"
            ]
            round_record.application_fields_download_available = round_config["application_fields_download_available"]
            round_record.display_logo_on_pdf_exports = round_config["display_logo_on_pdf_exports"]
            round_record.feedback_survey_config = round_config["feedback_survey_config"]
            round_record.mark_as_complete_enabled = round_config["mark_as_complete_enabled"]
            round_record.is_expression_of_interest = round_config["is_expression_of_interest"]
            round_record.eligibility_config = round_config["eligibility_config"]
            round_record.send_incomplete_application_emails = round_config.get(
                "send_incomplete_application_emails", True
            )
            round_record.eoi_decision_schema = round_config["eoi_decision_schema"]

            updated_rounds[round_config["id"]] = round_record

        else:
            # Insert new round record
            new_round = Round(
                id=round_config["id"],
                title_json=round_config["title_json"],
                short_name=round_config["short_name"],
                opens=round_config["opens"],
                assessment_start=round_config["assessment_start"],
                deadline=round_config["deadline"],
                application_reminder_sent=round_config["application_reminder_sent"],
                reminder_date=round_config["reminder_date"],
                fund_id=round_config["fund_id"],
                assessment_deadline=round_config["assessment_deadline"],
                prospectus=round_config["prospectus"],
                privacy_notice=round_config["privacy_notice"],
                contact_email=round_config["contact_email"],
                instructions_json=round_config["instructions_json"],
                project_name_field_id=round_config["project_name_field_id"],
                feedback_link=round_config["feedback_link"],
                application_guidance_json=round_config["application_guidance_json"],
                guidance_url=round_config["guidance_url"],
                all_uploaded_documents_section_available=round_config["all_uploaded_documents_section_available"],
                application_fields_download_available=round_config["application_fields_download_available"],
                display_logo_on_pdf_exports=round_config["display_logo_on_pdf_exports"],
                feedback_survey_config=round_config["feedback_survey_config"],
                mark_as_complete_enabled=round_config["mark_as_complete_enabled"],
                is_expression_of_interest=round_config["is_expression_of_interest"],
                eligibility_config=round_config["eligibility_config"],
                eoi_decision_schema=round_config["eoi_decision_schema"],
            )
            db.session.add(new_round)

            updated_rounds[round_config["id"]] = new_round

    print(f"Prepared rounds for insert: '{updated_rounds}'.")
    if commit:
        db.session.commit()
        print("DB changes committed")
    return updated_rounds


def insert_base_sections(APPLICATION_BASE_PATH, ASSESSMENT_BASE_PATH, round_id):
    """
    Insert base sections for a fund round.

    :param APPLICATION_BASE_PATH: The base path for the application sections.
    :param ASSESSMENT_BASE_PATH: The base path for the assessment sections.
    :param round_id: The id of the round to insert the sections for.
    :return: A dictionary of the inserted sections.
    """
    tree_base_sections = [
        {
            "section_name": {"en": "Application", "cy": "Application"},
            "tree_path": APPLICATION_BASE_PATH,
            "weighting": None,
        },
        {
            "section_name": {"en": "Assessment", "cy": "Assessment"},
            "tree_path": ASSESSMENT_BASE_PATH,
            "weighting": None,
        },
    ]

    updated_sections = {}
    for section in tree_base_sections:
        section_record = Section.query.filter(
            Section.path == Ltree(section["tree_path"]),
            Section.round_id == uuid.UUID(round_id),
        ).first()

        if section_record is not None:
            # Update existing section record
            section_record.round_id = round_id
            section_record.title_json = section["section_name"]
            section_record.weighting = section.get("weighting", None)
            section_record.requires_feedback = section.get("requires_feedback") or False

            updated_sections[section["tree_path"]] = section_record
        else:
            # Insert new section record
            new_section = Section(
                round_id=round_id,
                title_json=section["section_name"],
                weighting=section.get("weighting", None),
                path=Ltree(section["tree_path"]),
                requires_feedback=section.get("requires_feedback") or False,
            )
            db.session.add(new_section)

            updated_sections[section["tree_path"]] = new_section

    print(f"Prepared sections for insert: '{updated_sections}'.")
    return updated_sections


def insert_or_update_application_sections(round_id, sorted_application_sections: dict):
    print(f"Preparing insert for sections config: '{sorted_application_sections}'.")
    updated_sections = {}
    for section in sorted_application_sections:
        section_record = Section.query.filter(
            Section.path == Ltree(section["tree_path"]),
            Section.round_id == uuid.UUID(round_id),
        ).first()

        if section_record is not None:
            # Update existing section record
            section_id = section_record.id
            section_record.round_id = round_id
            section_record.title_json = section["section_name"]
            section_record.weighting = (section.get("weighting", None),)
            section_record.requires_feedback = section.get("requires_feedback") or False

            updated_sections[section_record.id] = section_record
            print(f"Prepared section UPDATE '{section_record}'.")
        else:
            # Insert new section record
            new_section = Section(
                round_id=round_id,
                title_json=section["section_name"],
                weighting=section.get("weighting", None),
                path=Ltree(section["tree_path"]),
                requires_feedback=section.get("requires_feedback") or False,
            )
            db.session.add(new_section)
            db.session.commit()
            section_id = new_section.id

            updated_sections[new_section.id] = new_section
            print(f"Prepared section INSERT '{new_section}'.")

        if section.get("form_name_json"):
            form_record = FormName.query.filter_by(section_id=section_id).first()
            if form_record is not None:
                form_record.form_name_json = section["form_name_json"]
                print(f"Updated form name information to {section['form_name_json']}.")
            else:
                new_form_record = FormName(form_name_json=section["form_name_json"], section_id=section_id)
                db.session.add(new_form_record)
                print(f"Inserted form name information: '{new_form_record}'.")
    db.session.commit()
    print("Section UPDATES and INSERTS Prepared for insert.")

    return updated_sections


def update_application_section_names(round_id, sorted_application_sections: List[dict], language_code=None):
    # TODO : Update this function to work with json objects in sorted_application_sections
    for section in sorted_application_sections:
        section_path = section["tree_path"]
        if language_code is None:
            split_section_name_list = section["section_name"].lower().split()
        else:
            split_section_name_list = section["section_name"][language_code].lower().split()
        try:
            float(split_section_name_list[0])
            split_section_name_list[1] = split_section_name_list[1].capitalize()
        except ValueError:
            split_section_name_list[0] = split_section_name_list[0].capitalize()
        new_section_name = " ".join(split_section_name_list)

        # Update the section name
        stmt = ""
        if language_code is None:
            stmt = (
                update(Section)
                .where(Section.round_id == round_id)
                .where(Section.path == Ltree(section_path))
                .values(title_json=new_section_name)
            )
        else:
            section["section_name"][language_code] = new_section_name
            stmt = (
                update(Section)
                .where(Section.round_id == round_id)
                .where(Section.path == Ltree(section_path))
                .values(title_json=section["section_name"])
            )
        db.session.execute(stmt)

    db.session.commit()


def __add__section_fields(field_section_links):
    stmt = (
        (
            postgres_insert(SectionField).values(
                field_id=bindparam("field_id"),
                section_id=bindparam("section_id"),
                display_order=bindparam("display_order"),
            )
        )
        .on_conflict_do_nothing(constraint="pk_section_field")
        .returning(
            SectionField.field_id,
            SectionField.section_id,
            SectionField.display_order,
        )
    )

    field_section_params = [
        {
            "field_id": section_link["field_id"],
            "section_id": section_link["section_id"],
            "display_order": section_link["display_order"],
        }
        for section_link in field_section_links
    ]

    inserted_field_section_result = db.session.execute(stmt, field_section_params).fetchall()
    return inserted_field_section_result


def insert_assessment_sections(round_id, assessment_config: list):
    sorted_assessment_sections = (
        assessment_config["sorted_scored_sections"] + assessment_config["sorted_unscored_sections"]
    )

    stmt = (
        insert(Section).values(
            round_id=bindparam("round_id"),
            title=bindparam("title"),
            weighting=bindparam("weighting"),
            path=bindparam("path"),
        )
    ).returning(Section.id)

    inserted_section_ids = []
    field_section_links = []
    for section in sorted_assessment_sections:
        section_params = {
            "round_id": round_id,
            "title": section["section_name"],
            "weighting": None,
            "path": Ltree(section["tree_path"]),
        }
        inserted_assessment_section_result = db.session.execute(stmt, section_params).fetchall()
        inserted_section_id = inserted_assessment_section_result[0][0]
        inserted_section_ids.append(inserted_section_id)
        if "fields" in section:
            for field in section["fields"]:
                field_section_links.append(
                    {
                        "field_id": field["form_json_id"],
                        "section_id": inserted_section_id,
                        "display_order": field["display_order"],
                    }
                )

    # flush so we can see the rows in the db before committing
    # db.session.commit()
    inserted_section_field_links = __add__section_fields(field_section_links)
    db.session.commit()
    return {
        "inserted_sections": inserted_section_ids,
        "inserted_section_field_links": inserted_section_field_links,
    }
