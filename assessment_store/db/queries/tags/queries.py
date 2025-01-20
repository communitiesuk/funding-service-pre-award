from typing import List

from flask import current_app
from sqlalchemy import distinct, func, or_
from sqlalchemy.exc import NoResultFound

from assessment_store.db.models.assessment_record.tag_association import TagAssociation
from assessment_store.db.models.tag.tag_types import TagType
from assessment_store.db.models.tag.tags import Tag
from db import db


def insert_tags(tags, fund_id, round_id):
    """Inserts tags associated with a round.

    Args:
        tags (list): A list of tag dictionaries [{
                "value": "",
                "purpose": "",
                "creator_user_id": "",
            }]
        round_id (str): The round to insert tags for.
        fund_id (str): The fund to insert tags for.

    Returns:
        inserted_tags (list): This method returns a list of inserted tags (the tag id and key)

    """
    inserted_tags = []
    for tag_data in tags:
        value = tag_data.get("value")
        creator_user_id = tag_data.get("creator_user_id")
        tag_type_id = tag_data.get("tag_type_id")

        # Create a new tag instance and trigger validation
        tag = Tag(
            value=value,
            fund_id=fund_id,
            round_id=round_id,
            creator_user_id=creator_user_id,
            type_id=tag_type_id,
        )
        db.session.add(tag)

        try:
            db.session.flush()  # Flush changes to trigger validation
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error inserting tag '{value}': {str(e)}") from e

        inserted_tags.append(tag)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error inserting tags: {str(e)}") from e
    return inserted_tags


def update_tags(tags, fund_id, round_id):
    """Takes a list of tag updates and applies them to the tag_id specified.

    Args:
        tags (list): A list of tag update dictionaries [{
                "id": "",
                "value": "",
                "purpose": "",
                "creator_user_id": "",
                "active": "",
            }]
        round_id (str): The round to insert tags for.
        fund_id (str): The fund to insert tags for.

    Returns:
        updated (list): This method returns a list of updated tags (the tag id and key)

    """
    updated_tags = []

    for tag_data in tags:
        tag_id = tag_data["id"]
        tag_value = tag_data.get("value")
        tag_type_id = tag_data.get("tag_type_id")
        creator_user_id = tag_data.get("creator_user_id")
        active_status = tag_data.get("active")

        try:
            # Check if the tag already exists in the database
            tag = (
                db.session.query(Tag)
                .filter_by(
                    id=tag_id,
                )
                .one()
            )

            # Update the existing tag's attributes
            tag.value = tag_value if tag_value is not None else tag.value
            tag.creator_user_id = creator_user_id if creator_user_id is not None else tag.creator_user_id
            tag.type_id = tag_type_id if tag_type_id is not None else tag.type_id
            tag.active = active_status if active_status is not None else tag.active

        except NoResultFound as e:
            # If the tag doesn't exist, raise an error
            raise ValueError(
                f"Tag with id '{tag_id}' does not exist for fund_id '{fund_id}' and round_id '{round_id}'."
            ) from e

        updated_tags.append(tag)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error updating tags: {str(e)}") from e
    return updated_tags


def select_tags_for_fund_round(
    fund_id: str,
    round_id: str,
    tag_purpose: str,
    tag_status: bool,
    search_term: str,
    search_in: str,
) -> List[Tag]:
    statement = (
        db.session.query(
            Tag.id,
            Tag.value,
            Tag.active,
            Tag.type_id,
            Tag.fund_id,
            Tag.round_id,
            Tag.creator_user_id,
            Tag.created_at,
            TagType.purpose.label("purpose"),
            TagType.description.label("description"),
        )
        .join(TagType, Tag.type_id == TagType.id)
        .where(Tag.fund_id == fund_id)
        .where(Tag.round_id == round_id)
    )
    if search_term != "":
        current_app.logger.info(
            "Performing tag search on search term: %(search_term)s in fields %(search_in)s",
            dict(search_term=search_term, search_in=search_in),
        )
        # using % for sql LIKE search
        search_term = search_term.replace(" ", "%")

        filters = []
        if "value" in search_in:
            filters.append(Tag.value.ilike(f"%{search_term}%"))

        statement = statement.filter(or_(*filters))

    if tag_purpose.upper() != "ALL":
        statement = statement.where(TagType.purpose == tag_purpose.upper())

    if tag_status is not None:
        statement = statement.where(Tag.active == tag_status)
    tags = statement.all()

    return tags


def get_tag_by_id(fund_id: str, round_id: str, tag_id: str) -> Tag:
    try:
        # Select each unique tag TO tag_association
        # return only the latest tag TO tag_association (each association/disassociation is a new record)
        # filter to match on only the supplied tag_id ^
        # filter out any tag-tag_association that is not associated
        subquery = (
            db.session.query(
                TagAssociation.tag_id,
                TagAssociation.application_id,
                func.max(TagAssociation.created_at).label("max_created_at"),
            )
            .group_by(TagAssociation.application_id, TagAssociation.tag_id)
            .filter(TagAssociation.tag_id == tag_id)
            .filter(TagAssociation.associated == True)  # noqa
            .subquery()
        )

        # Use the subquery in the main query
        return (
            db.session.query(
                Tag.id,
                Tag.value,
                Tag.active,
                Tag.type_id,
                Tag.fund_id,
                Tag.round_id,
                Tag.creator_user_id,
                Tag.created_at,
                TagType.purpose.label("purpose"),
                TagType.description.label("description"),
                func.count(distinct(subquery.c.application_id)).label("tag_association_count"),
            )
            .join(TagType, Tag.type_id == TagType.id)
            .outerjoin(subquery, Tag.id == subquery.c.tag_id)
            .filter(Tag.fund_id == fund_id)
            .filter(Tag.round_id == round_id)
            .filter(Tag.id == tag_id)
            .group_by(
                Tag.id,
                Tag.value,
                Tag.active,
                Tag.type_id,
                Tag.fund_id,
                Tag.round_id,
                Tag.creator_user_id,
                Tag.created_at,
                TagType.purpose,
                TagType.description,
            )
            .one()
        )
    except NoResultFound as e:
        current_app.log_exception(e)
        return None


def select_tags_types() -> List[TagType]:
    return db.session.query(TagType).all()
