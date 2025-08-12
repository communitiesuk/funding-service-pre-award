"""Queries which are performed on the `assessment_records` table.

Joins allowed.

"""

from datetime import datetime, timezone
from typing import Dict, List

from bs4 import BeautifulSoup
from dateutil import parser
from flask import current_app
from sqlalchemy import String, and_, cast, desc, exc, func, or_, select
from sqlalchemy.orm import aliased, defer, load_only, selectinload

from pre_award.assessment_store.db.models.assessment_record import AssessmentRecord, TagAssociation
from pre_award.assessment_store.db.models.assessment_record.allocation_association import AllocationAssociation
from pre_award.assessment_store.db.models.assessment_record.enums import Status
from pre_award.assessment_store.db.models.flags.flag_update import FlagStatus
from pre_award.assessment_store.db.models.score import Score
from pre_award.assessment_store.db.models.tag.tag_types import TagType
from pre_award.assessment_store.db.models.tag.tags import Tag
from pre_award.assessment_store.db.queries.assessment_records._helpers import (
    filter_tags,
    get_existing_tags,
    update_tag_associations,
)
from pre_award.assessment_store.db.schemas import (
    AssessmentRecordMetadata,
    AssessmentSubCriteriaMetadata,
    AssessorTaskListMetadata,
)
from pre_award.assessment_store.services.data_services import get_account_name
from pre_award.db import db


def get_metadata_for_application(
    application_id: str,
) -> List[Dict]:
    statement = (
        select(AssessmentRecord)
        .options(defer(AssessmentRecord.jsonb_blob))
        .where(
            AssessmentRecord.application_id == application_id,
            AssessmentRecord.is_withdrawn == False,  # noqa: E712
        )
    )

    result = db.session.scalar(statement)
    metadata_serializer = AssessmentRecordMetadata(exclude=("jsonb_blob", "application_json_md5"))
    return metadata_serializer.dump(result)


def get_assessment_record(app_id) -> AssessmentRecord | None:
    return AssessmentRecord.query.get(app_id)


def get_metadata_for_fund_round_id(  # noqa: C901 - historical sadness
    fund_id: str,
    round_id: str,
    search_term: str = "",
    asset_type: str = "",
    status: str = "",
    search_in: str = "",
    funding_type: str = "",
    countries: List[str] | None = None,
    filter_by_tag: str = "",
    country: str = "",
    region: str = "",
    local_authority: str = "",
    cohort: str = "",
    publish_datasets: str = "",
    datasets: str = "",
    team_in_place: str = "",
    joint_application: str = "",
) -> List[Dict]:
    """get_metadata_for_fund_round_id Executes a query on assessment records which
    returns all rows matching the given fund_id and round_id. Has optional
    parameters of search_term, asset_type and status for filterting. Excludes
    irrelevant columns such as `db.models.AssessmentRecord.jsonb_blob`.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A list of dictionaries.

    """
    if countries is None:
        countries = ["all"]

    statement = (
        select(AssessmentRecord)
        # Dont load json into memory
        .options(
            defer(AssessmentRecord.jsonb_blob),
            selectinload(AssessmentRecord.qa_complete),
            selectinload(AssessmentRecord.flags),
            selectinload(AssessmentRecord.user_associations),
            selectinload(AssessmentRecord.tag_associations).selectinload(TagAssociation.tag).selectinload(Tag.tag_type),
        )
        .where(
            AssessmentRecord.fund_id == fund_id,
            AssessmentRecord.round_id == round_id,
            AssessmentRecord.is_withdrawn == False,  # noqa: E712
        )
    )
    if search_term != "":
        current_app.logger.info(
            "Performing assessment search on search term: %(search_term)s in fields %(search_in)s",
            dict(search_term=search_term, search_in=search_in),
        )
        search_term = search_term.replace(" ", "%")

        filters = []
        if "short_id" in search_in:
            filters.append(AssessmentRecord.short_id.ilike(f"%{search_term}%"))
        if "project_name" in search_in:
            filters.append(AssessmentRecord.project_name.ilike(f"%{search_term}%"))
        if "organisation_name" in search_in:
            filters.append(func.cast(AssessmentRecord.organisation_name, String).ilike(f"%{search_term}%"))

        statement = statement.filter(or_(*filters))

    if cohort != "ALL" and cohort != "":
        statement = statement.filter(or_(func.cast(AssessmentRecord.cohort, String).ilike(f"%{cohort}%")))

    if filter_by_tag and filter_by_tag.casefold() != "all":
        assessment_records_by_tag_id = (
            db.session.query(AssessmentRecord)
            .filter(TagAssociation.associated == True)  # noqa E712
            .join(TagAssociation)
            .filter(
                TagAssociation.tag_id == filter_by_tag,
                TagAssociation.associated == True,  # noqa E712
            )
            .all()
        )
        record_ids_with_tag_id = [record.application_id for record in assessment_records_by_tag_id]
        statement = statement.where(AssessmentRecord.application_id.in_(record_ids_with_tag_id))

    if "all" not in countries:
        current_app.logger.info("Performing assessment search on countries: %(countries)s.", dict(countries=countries))
        statement = statement.where(AssessmentRecord.location_json_blob["country"].astext.ilike(func.any_(countries)))

    if asset_type != "ALL" and asset_type != "":
        current_app.logger.info(
            "Performing assessment search on asset type: %(asset_type)s.", dict(asset_type=asset_type)
        )
        statement = statement.where(AssessmentRecord.asset_type == asset_type)

    if country != "" and country != "ALL":
        current_app.logger.info("Performing assessment search on country: %(country)s.", dict(country=country))
        statement = statement.where(AssessmentRecord.location_json_blob["country"].astext == country)

    if region != "" and region != "ALL":
        current_app.logger.info("Performing assessment search on region: %(region)s.", dict(region=region))
        statement = statement.where(AssessmentRecord.location_json_blob["region"].astext == region)

    if datasets != "" and datasets != "ALL":
        datasets = True if str(datasets).lower() == "yes" or datasets is True else False
        current_app.logger.info("Performing assessment search on datasets: %(datasets)s.", dict(datasets=datasets))
        statement = statement.where(cast(AssessmentRecord.datasets, String) == str(datasets).lower())

    if publish_datasets != "" and publish_datasets != "ALL":
        current_app.logger.info(
            "Performing assessment search on publish_datasets: %(publish_datasets)s.",
            dict(publish_datasets=publish_datasets),
        )
        if publish_datasets == "None":
            statement = statement.where(AssessmentRecord.publish_datasets.is_(None))
        else:
            statement = statement.where(cast(AssessmentRecord.publish_datasets, String).ilike(f"%{publish_datasets}%"))

    if team_in_place != "" and team_in_place != "ALL":
        team_in_place = True if str(team_in_place).lower() == "yes" or team_in_place is True else False
        current_app.logger.info(
            "Performing assessment search on team_in_place: %(team_in_place)s.", dict(team_in_place=team_in_place)
        )
        statement = statement.where(cast(AssessmentRecord.team_in_place, String) == str(team_in_place).lower())

    if local_authority != "" and local_authority != "ALL":
        current_app.logger.info(
            "Performing assessment search on local_authority: %(local_authority)s.",
            dict(local_authority=local_authority),
        )

        subquery = (
            select(AssessmentRecord.application_id).where(
                func.jsonb_path_exists(
                    AssessmentRecord.jsonb_blob,
                    f'$.forms[*].questions[*].fields[*] ? (@.key == "nURkuc"'
                    f'|| @.key == "WLddBt" && @.answer == "{local_authority}")',
                ),
            )
        ).subquery()

        statement = statement.where(AssessmentRecord.application_id.in_(subquery))

    if joint_application != "" and joint_application != "ALL" and joint_application in ["true", "false"]:
        current_app.logger.info(
            "Performing assessment search on joint_application: %(joint_application)s.",
            dict(joint_application=joint_application),
        )

        subquery = (
            select(AssessmentRecord.application_id).where(
                func.jsonb_path_exists(
                    AssessmentRecord.jsonb_blob,
                    f'$.forms[*].questions[*].fields[*] ? (@.key == "luWnQp" && @.answer == {joint_application})',
                ),
            )
        ).subquery()

        statement = statement.where(AssessmentRecord.application_id.in_(subquery))

    if funding_type != "ALL" and funding_type != "":
        current_app.logger.info(
            "Performing assessment search on funding type: %(funding_type)s.", dict(funding_type=funding_type)
        )
        # TODO SS figure out how to stop double quoting this - it works but is ugly
        # it's because when we retrieve the json element as funding_type, we get it as a json element, not pure text,
        # so it has the double quotes from the json so we have to include them in the comparison
        statement = statement.where(func.cast(AssessmentRecord.funding_type, String) == f'"{funding_type}"')

    raw_results = db.session.execute(statement)
    assessment_metadatas = raw_results.unique().scalars().all()

    if status != "ALL":
        filter_assessments = []
        for assessment in assessment_metadatas:
            all_latest_status = [flag.latest_status for flag in assessment.flags]
            is_qa_complete = True if assessment.qa_complete else False

            raised_flags = all_latest_status.count(FlagStatus.RAISED)

            # Set default display status to workflow status name e.g., "Ready to review"
            display_status = assessment.workflow_status.name

            # If QA is complete, update display status
            display_status = "QA_COMPLETED" if is_qa_complete else display_status

            # If flagged, update display status
            if assessment.workflow_status == Status.CHANGE_REQUESTED:
                # A change request technically counts as a flag but is not a "real" flag
                match raised_flags:
                    case 0:
                        pass
                    case 1:
                        display_status = "CHANGE_REQUESTED"
                    case 2:
                        display_status = "FLAGGED"
                    case _:
                        display_status = "MULTIPLE_FLAGS"
            else:
                match raised_flags:
                    case 0:
                        pass
                    case 1:
                        display_status = "FLAGGED"
                    case _:
                        display_status = "MULTIPLE_FLAGS"

            # Stopped status overrides all!
            display_status = "STOPPED" if FlagStatus.STOPPED in all_latest_status else display_status
            if display_status == status:
                filter_assessments.append(assessment)

        assessment_metadatas = filter_assessments

    metadata_serialiser = AssessmentRecordMetadata(exclude=("jsonb_blob", "application_json_md5"))

    assessment_metadatas = [
        metadata_serialiser.dump(app_metadata) | {"is_qa_complete": True if app_metadata.qa_complete else False}
        for app_metadata in assessment_metadatas
    ]

    assessment_metadatas_with_recent_tags = update_tag_associations(assessment_metadatas)
    return assessment_metadatas_with_recent_tags


def delete_assessment_record(app_id):
    """Delete the assessment record with the given ID from the database.

    Returns True if the record was successfully deleted, or False
    otherwise.

    """
    try:
        assessment_record = AssessmentRecord.query.get(app_id)
        if assessment_record is not None:
            db.session.delete(assessment_record)
            db.session.commit()
            return True
    except Exception as e:
        print(f"Error deleting assessment record: {e}")
    return False


def find_answer_by_key_runner(field_key: str, app_id: str) -> List[tuple]:
    """find_answer_by_key_runner Given an application id `app_id` and a field to
    search for `app_id` we return the matching field object (A json with keys
    {key, answer, title, type}) within an SQLAlchemy result.

    :param field_key: The unique key of the field.
    :type field_key: str
    :param app_id: The application id of the queried row.
    :type app_id: str
    :return: The whole field object of the found field. Returned as a
        SQLAlchemy result.
    :rtype: List[tuple]

    """

    return (
        db.session.query(
            func.jsonb_path_query_first(
                AssessmentRecord.jsonb_blob,
                f'$.forms[*].questions[*].fields[*] ? (@.key == "{field_key}")',
            )
        )
        .filter(AssessmentRecord.application_id == app_id)
        .one()
    )


def find_assessor_task_list_state(application_id: str) -> dict:
    """find_assessment Given an application id `application_id` we return the
    matching row from the `assessment_records` table.

    :param application_id: The application id of the queried row.
    :type application_id: str
    :return: The matching row from the `assessment_records` table.
    :rtype: dict

    """

    stmt = (
        select(AssessmentRecord)
        .where(
            AssessmentRecord.application_id == application_id,
            AssessmentRecord.is_withdrawn == False,  # noqa: E712
        )
        .options(
            load_only(
                AssessmentRecord.short_id,
                AssessmentRecord.project_name,
                AssessmentRecord.workflow_status,
                AssessmentRecord.jsonb_blob,
                AssessmentRecord.fund_id,
                AssessmentRecord.round_id,
                AssessmentRecord.funding_amount_requested,
                AssessmentRecord.language,
            )
        )
    )

    assessment_record = db.session.scalar(stmt)

    assessment_record_json = AssessorTaskListMetadata(
        only=(
            "short_id",
            "project_name",
            "date_submitted",
            "workflow_status",
            "fund_id",
            "round_id",
            "funding_amount_requested",
            "language",
            "is_deleted",
        )
    ).dump(assessment_record)

    return assessment_record_json


def get_assessment_sub_critera_state(application_id: str) -> dict:
    """Given an application id `application_id` we return the relevant record from
    the `assessment_records` table with state related to the assessments
    sub_criteria context.

    :param application_id: The application id of the queried row.
    :type application_id: str
    :return: The matching row from the `assessment_records` table.
    :rtype: dict

    """

    stmt = (
        select(AssessmentRecord)
        .where(
            AssessmentRecord.application_id == application_id,
            AssessmentRecord.is_withdrawn == False,  # noqa: E712
        )
        .options(
            load_only(
                AssessmentRecord.funding_amount_requested,
                AssessmentRecord.project_name,
                AssessmentRecord.fund_id,
                AssessmentRecord.workflow_status,
                AssessmentRecord.short_id,
            )
        )
    )

    assessment_record = db.session.scalar(stmt)

    assessment_record_json = AssessmentSubCriteriaMetadata(
        only=(
            "funding_amount_requested",
            "project_name",
            "fund_id",
            "workflow_status",
            "short_id",
        )
    ).dump(assessment_record)

    return assessment_record_json


def get_application_jsonb_blob(application_id: str) -> dict:
    stmt = (
        select(AssessmentRecord)
        .where(
            AssessmentRecord.application_id == application_id,
            AssessmentRecord.is_withdrawn == False,  # noqa: E712
        )
        .options(load_only(AssessmentRecord.jsonb_blob))
    )
    application_jsonb_blob = db.session.scalar(stmt)
    application_json = AssessorTaskListMetadata().dump(application_jsonb_blob)
    return application_json


def update_status_to_completed(application_id):
    current_app.logger.info(
        "Updating application status to COMPLETED for application: %(application_id)s.",
        dict(application_id=application_id),
    )
    update_application_status(application_id=application_id, status=Status.COMPLETED)


def update_application_status(application_id: str, status: Status):
    db.session.query(AssessmentRecord).filter(AssessmentRecord.application_id == application_id).update(
        {AssessmentRecord.workflow_status: status},
        synchronize_session=False,
    )
    db.session.commit()


def get_assessment_records_score_data_by_round_id(round_id, selected_fields=None, language=None):  # noqa
    """Retrieve the latest scores and associated information for each subcriteria
    of AssessmentRecords matching the given round_id.

    Parameters:
        round_id (UUID): The ID of the round to filter AssessmentRecords.

    Returns:
        list: A list of dictionaries, each containing the latest score and its associated
        information for each subcriteria of the AssessmentRecords that match the given round_id.

    """
    default_fields = [
        "Application ID",
        "Short ID",
        "Score",
        "Score Subcriteria",
        "Score Justification",
        "Score Date",
        "Score Time",
        "Scorer Name",
    ]

    # If selected_fields is not provided, use the default_fields.
    if selected_fields is None:
        selected_fields = default_fields

    selected_fields = [field for field in selected_fields if field in default_fields]
    subquery = (
        db.session.query(
            Score.application_id,
            Score.sub_criteria_id,
            func.max(Score.date_created).label("latest_date_created"),
        )
        .group_by(Score.application_id, Score.sub_criteria_id)
        .subquery()
    )

    query = (
        db.session.query(Score)
        .join(
            subquery,
            and_(
                Score.application_id == subquery.c.application_id,
                Score.sub_criteria_id == subquery.c.sub_criteria_id,
                Score.date_created == subquery.c.latest_date_created,
            ),
        )
        .join(
            AssessmentRecord,
            Score.application_id == AssessmentRecord.application_id,
        )
        .filter(
            AssessmentRecord.round_id == round_id,
            AssessmentRecord.is_withdrawn == False,  # noqa: E712
        )
    )

    if language is not None:
        query = query.filter(AssessmentRecord.language == language)

    latest_scores = query.all()

    output = []
    for score in latest_scores:
        score_data = {
            "Application ID": score.application_id,
            "Short ID": AssessmentRecord.query.get(score.application_id).short_id,
            "Score Subcriteria": score.sub_criteria_id,
            "Score": score.score,
            "Score Justification": score.justification,
            "Score Date": score.date_created.strftime("%d/%m/%Y"),
            "Score Time": score.date_created.strftime("%H:%M:%S"),
            "Scorer Name": get_account_name(score.user_id),
        }

        selected_score_data = {field: score_data[field] for field in selected_fields}
        output.append(selected_score_data)
    return output


def create_tag(application_id, tag_id, associated, user_id):
    new_tag = TagAssociation(
        application_id=application_id,
        tag_id=tag_id,
        associated=associated,
        user_id=user_id,
    )
    db.session.add(new_tag)


def associate_assessment_tags(application_id, tags: List):
    _existing_tags = get_existing_tags(application_id)
    for incoming_tag in tags:
        incoming_user_id = incoming_tag.get("user_id")
        incoming_tag_id = incoming_tag.get("id")

        if incoming_tag_id and not _existing_tags:
            # If no existing tags are found, create a new tag(s) with incoming tags info.
            current_app.logger.info(
                "Creating new tag(s) for %(incoming_tag_id)s", dict(incoming_tag_id=incoming_tag_id)
            )
            create_tag(application_id, incoming_tag_id, True, incoming_user_id)

        if incoming_tag_id and _existing_tags:
            # Check if the tag already exists, otherwise, create a new associated tag.
            tag_exists = incoming_tag_id in _existing_tags.keys()
            if tag_exists:
                # Find the most recent version of the tag.
                most_recent_tag = max(
                    _existing_tags[incoming_tag_id],
                    key=lambda x: x[0],
                )[1]
                # If it's already associated, skip, otherwise, create a new associated tag.
                if most_recent_tag.associated:
                    current_app.logger.info(
                        "Tag is alreday associated: %(tag_id)s", dict(tag_id=most_recent_tag.tag_id)
                    )
                else:
                    current_app.logger.info(
                        "Creating new tag: %(incoming_tag_id)s", dict(incoming_tag_id=incoming_tag_id)
                    )
                    create_tag(
                        application_id,
                        incoming_tag_id,
                        True,
                        incoming_user_id,
                    )
            else:
                current_app.logger.info("Creating new tag: %(incoming_tag_id)s", dict(incoming_tag_id=incoming_tag_id))
                create_tag(application_id, incoming_tag_id, True, incoming_user_id)

        if not incoming_tag_id:
            filterted_tags = filter_tags(tags, _existing_tags)
            for filterted_tag in filterted_tags:
                most_recent_tag = max(filterted_tag, key=lambda x: x[0])[1]
                if most_recent_tag.associated:
                    current_app.logger.info(
                        "Dis-associating existing associated tag_id: %(tag_id)s",
                        dict(tag_id=most_recent_tag.tag_id),
                    )
                    create_tag(
                        application_id,
                        most_recent_tag.tag_id,
                        False,
                        incoming_user_id,
                    )
    db.session.commit()

    # Retrieve all records for a specific application_id
    subquery = (
        TagAssociation.query.filter(TagAssociation.application_id == application_id)
        .order_by(TagAssociation.tag_id, desc(TagAssociation.created_at))
        .distinct(TagAssociation.tag_id)
        .subquery()
    )

    # Use a subquery to get the most recent record for each tag_id
    alias = aliased(TagAssociation, subquery)
    recent_records = db.session.query(alias).order_by(alias.tag_id, desc(alias.created_at)).distinct(alias.tag_id).all()

    # Check if the most recent record for each tag_id has associated set to True
    associated_tags = [record for record in recent_records if record.associated]
    return associated_tags


def select_active_tags_associated_with_assessment(application_id):
    try:
        # Step 1: Selecting columns and creating aliases
        query = db.session.query(
            Tag.id.label("tag_id"),
            Tag.value,
            Tag.active,
            TagType.purpose,
            TagType.description,
            TagAssociation.associated,
            TagAssociation.user_id,
            AssessmentRecord.application_id,
            func.max(TagAssociation.created_at).label("_created_at"),
        )

        # Step 2: Joining tables
        query = (
            query.join(
                AssessmentRecord,
                TagAssociation.application_id == AssessmentRecord.application_id,
            )
            .join(Tag, Tag.id == TagAssociation.tag_id)
            .join(TagType, Tag.type_id == TagType.id)
        )

        # Step 3: Filtering by application_id
        query = query.filter(
            AssessmentRecord.application_id == application_id,
        )

        # Step 4: Group data based on tags and related info.
        query = query.group_by(
            Tag.id,
            Tag.value,
            Tag.active,
            TagType.purpose,
            TagType.description,
            TagAssociation.associated,
            TagAssociation.user_id,
            AssessmentRecord.application_id,
        )

        # Step 5: Getting the most recent created_at for each tag_id
        subquery = (
            db.session.query(
                TagAssociation.tag_id,
                func.max(TagAssociation.created_at).label("_created_at"),
            )
            .filter(
                TagAssociation.application_id == application_id,
            )
            .group_by(TagAssociation.tag_id)
            .subquery()
        )

        query = query.join(
            subquery,
            and_(
                TagAssociation.tag_id == subquery.c.tag_id,
                TagAssociation.created_at == subquery.c._created_at,
            ),
        )

        # Step 6: Executing the whole query
        tag_associations = query.all()

        # Step 7: Check if the first record for each tag_id has associated set to True and tag is active
        associated_tags = [record for record in tag_associations if record.active and record.associated]

        return associated_tags

    except Exception as e:
        current_app.logger.exception("Error")
        raise e


def select_all_tags_associated_with_application(application_id):
    tag_associations = (
        db.session.query(
            Tag.id.label("tag_id"),
            Tag.value,
            TagType.purpose,
            TagType.description,
            TagAssociation.associated,
            TagAssociation.user_id,
            TagAssociation.created_at,
            AssessmentRecord.application_id,
        )
        .join(
            AssessmentRecord,
            TagAssociation.application_id == AssessmentRecord.application_id,
        )
        .join(Tag, Tag.id == TagAssociation.tag_id)
        .join(TagType, Tag.type_id == TagType.id)
        .filter(
            AssessmentRecord.application_id == application_id,
        )
        .all()
    )

    db.session.commit()
    return tag_associations


def get_assessment_export_data(fund_id: str, round_id: str, report_type: str, list_of_fields: dict):
    en_statement = select(AssessmentRecord).where(
        AssessmentRecord.fund_id == fund_id,
        AssessmentRecord.round_id == round_id,
        AssessmentRecord.language == "en",
        AssessmentRecord.is_withdrawn == False,  # noqa: E712
    )

    en_assessment_metadatas = db.session.scalars(en_statement).all()

    cy_statement = select(AssessmentRecord).where(
        AssessmentRecord.fund_id == fund_id,
        AssessmentRecord.round_id == round_id,
        AssessmentRecord.language == "cy",
        AssessmentRecord.is_withdrawn == False,  # noqa: E712
    )

    cy_assessment_metadatas = db.session.scalars(cy_statement).all()

    en_list = get_export_data(
        round_id=round_id,
        report_type=report_type,
        list_of_fields=list_of_fields,
        assessment_metadatas=en_assessment_metadatas,
        language="en",
    )
    cy_list = get_export_data(
        round_id=round_id,
        report_type=report_type,
        list_of_fields=list_of_fields,
        assessment_metadatas=cy_assessment_metadatas,
        language="cy",
    )

    obj = {"en_list": en_list, "cy_list": cy_list}
    return obj


def get_export_data(  # noqa: C901 - historical sadness
    round_id: str,
    report_type: str,
    list_of_fields: dict,
    assessment_metadatas: list,
    language: str,  # noqa
) -> List[Dict]:  # noqa
    form_fields = list_of_fields.get(report_type, {}).get("form_fields", {})
    field_ids = form_fields.keys()
    final_list = []

    for assessment in assessment_metadatas:
        iso_datetime = parser.isoparse(assessment.jsonb_blob["date_submitted"])
        formatted_date = iso_datetime.strftime("%d/%m/%Y %H:%M:%S")

        applicant_info = {
            "Application ID": assessment.application_id,
            "Short ID": assessment.short_id,
            "Date Submitted": formatted_date,
        }
        if len(form_fields) != 0:
            forms = assessment.jsonb_blob["forms"]
            for form in forms:
                questions = form["questions"]
                for question in questions:
                    fields = question["fields"]
                    for field in fields:
                        if field["key"] in field_ids:
                            title = form_fields[field["key"]][language]["title"]
                            field_type = form_fields[field["key"]][language].get("field_type", field["type"])

                            if "answer" not in field:  # we use a blank string is there's no answer.
                                applicant_info[title] = ""
                                continue

                            # filter 'null' values from the address field
                            # TODO: Remove this filter after FS-4021
                            if field["answer"] and field_type == "ukAddressField":
                                address_parts = field["answer"].split(", ")
                                answer = ", ".join([part for part in address_parts if part != "null"])
                            elif field["answer"] and field_type == "uk_postcode":
                                answer = field["answer"].split(", ")[-1]
                            else:
                                answer = field["answer"]

                            if answer and field_type == "freeText":  # for `freeText` type, extract the plain text
                                answer = BeautifulSoup(answer, "html.parser").get_text(
                                    strip=True
                                )  # Extract text, strip extra whitespace
                            if field_type == "list" and not isinstance(
                                answer, bool
                            ):  # Adding check for bool since yesno fields are considered lists
                                answer = format_lists(answer)

                            if field_type == "sum_list" and isinstance(field["answer"], list):
                                answer = 0
                                field_to_sum = form_fields[field["key"]][language].get("field_to_sum", None)
                                if not field_to_sum:
                                    applicant_info[title] = ""
                                    continue
                                for sum_item in field["answer"]:
                                    answer += int(sum_item[field_to_sum])

                            if field_type == "MultiInputField" and isinstance(answer, list):
                                child_map = form_fields[field["key"]][language].get("formatted_children", "")
                                if title not in applicant_info:
                                    applicant_info[title] = ""
                                for child in answer:
                                    for child_key, child_value in child.items():
                                        child_title = child_map.get(child_key, child_key)
                                        # Append each child value as a new line in the same column
                                        applicant_info[title] += f"({child_title}): {child_value}\n"

                                applicant_info[title].strip()
                                continue
                            else:
                                applicant_info[title] = str(answer)
                            applicant_info[title] = answer
            applicant_info = add_missing_elements_with_empty_values(applicant_info, form_fields, language)
        final_list.append(applicant_info)

    if report_type == "OUTPUT_TRACKER":
        score_info_output = get_assessment_records_score_data_by_round_id(
            round_id,
            list_of_fields[report_type].get("score_fields", None),
            language,
        )
        final_list = combine_dicts(final_list, score_info_output)

    return final_list


# adds missing elements for use in the csv
def add_missing_elements_with_empty_values(applicant_info, form_fields, language):
    result_data = applicant_info.copy()

    for _key, value in form_fields.items():
        title = value[language]["title"]
        if title not in result_data:
            result_data[title] = ""
    return result_data


def format_lists(answer):
    formatted_elements = []
    indent = " " * 5
    for index, element in enumerate(answer, start=1):
        separator = f"{indent}." if index > 1 else "."
        formatted_elements.append(f"{separator} {element}")

    return "\n".join(formatted_elements)


def combine_dicts(applications_list, scores_list):
    combined_list = []

    if len(applications_list) == 0 and len(scores_list) == 0:
        return combined_list

    for application in applications_list:
        app_id = application["Application ID"]
        matching_scores = [score for score in scores_list if score["Application ID"] == app_id]
        if matching_scores:
            for score in matching_scores:
                combined_element = {**application, **score}
                combined_list.append(combined_element)
        else:
            application_with_nulls = {**application, "Score": "No scores yet"}
            combined_list.append(application_with_nulls)

    return combined_list


def get_user_application_associations(application_id=None, user_id=None, assigner_id=None, active=None):
    query = db.session.query(AllocationAssociation)
    if application_id:
        query = query.filter(AllocationAssociation.application_id == application_id)

    if user_id:
        query = query.filter(AllocationAssociation.user_id == user_id)

    if assigner_id:
        query = query.filter(AllocationAssociation.assigner_id == assigner_id)

    if active is not None:
        query = query.filter(AllocationAssociation.active == active)

    return query.all()


def create_user_application_association(application_id, user_id, assigner_id):
    allocation_association = AllocationAssociation(
        user_id=user_id,
        application_id=application_id,
        assigner_id=assigner_id,
        active=True,
        log={
            datetime.now(tz=timezone.utc).isoformat(): {
                "status": "activated",
                "assigner": str(assigner_id),
            }
        },
    )
    try:
        db.session.add(allocation_association)
        db.session.commit()
        db.session.refresh(allocation_association)
    except exc.IntegrityError:
        db.session.rollback()
        return None

    return allocation_association


def update_user_application_association(application_id, user_id, active, assigner_id):
    allocation_association = (
        db.session.query(AllocationAssociation)
        .filter(
            AllocationAssociation.application_id == application_id,
            AllocationAssociation.user_id == user_id,
        )
        .one_or_none()
    )
    allocation_association.assigner_id = assigner_id
    allocation_association.active = active
    allocation_association.log = {
        **allocation_association.log,
        datetime.now(tz=timezone.utc).isoformat(): {
            "status": "activated" if active else "deactivated",
            "assigner": str(assigner_id),
        },
    }
    db.session.commit()
    db.session.refresh(allocation_association)

    return allocation_association


def check_all_change_requests_accepted(application_id):
    application = db.session.scalar(select(AssessmentRecord).where(AssessmentRecord.application_id == application_id))

    change_requests = application.change_requests
    scores = application.scores

    # if a section has been accepted, we "close" any change requests regardless of the state
    # they are in (RAISED or RESOLVED)
    accepted_sections = set(score.sub_criteria_id for score in scores if score.score > 0)

    # Change requests may either be resolved by the applicant, or in a raised (unresolved) state by the assessor
    requested_changes_sections = set(
        section for change_request in change_requests for section in change_request.sections_to_flag
    )
    remaining_sections = requested_changes_sections - accepted_sections

    return len(remaining_sections) == 0
