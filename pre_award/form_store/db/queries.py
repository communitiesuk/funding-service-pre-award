from datetime import datetime
from typing import List

from sqlalchemy.sql import func

from pre_award.db import db
from pre_award.form_store.db.models.form_definition import FormDefinition


def get_all_forms() -> List[FormDefinition]:
    """
    Retrieve all forms from the database.

    Returns:
        List[FormDefinition]: List of all form definitions
    """
    return db.session.query(FormDefinition).all()


def get_form_by_url_path(url_path: str) -> FormDefinition:
    """
    Retrieve a form by its URL path.

    Args:
        url_path (str): The URL path of the form

    Returns:
        FormDefinition: The form definition

    Raises:
        NoResultFound: If no form with the given URL path exists
    """
    return db.session.query(FormDefinition).filter(FormDefinition.url_path == url_path).one()


def create_or_update_form(url_path: str, display_name: str, form_json: dict) -> FormDefinition:
    """
    Create a new form or update an existing form's draft.

    Args:
        url_path (str): The URL path of the form
        display_name (str): The display name of the form
        form_json (dict): The form JSON data

    Returns:
        FormDefinition: The created or updated form definition
    """
    existing_form = db.session.query(FormDefinition).filter(FormDefinition.url_path == url_path).first()

    if existing_form:
        # Update existing form's draft
        existing_form.draft_json = form_json
        existing_form.display_name = display_name
        existing_form.updated_at = func.now()
        db.session.commit()
        return existing_form
    else:
        # Create new form
        new_form = FormDefinition(url_path=url_path, display_name=display_name, draft_json=form_json, published_json={})
        db.session.add(new_form)
        db.session.commit()
        return new_form


def publish_form(url_path: str) -> FormDefinition:
    """
    Publish a form by copying draft_json to published_json.

    Args:
        url_path (str): The URL path of the form to publish

    Returns:
        FormDefinition: The published form definition

    Raises:
        NoResultFound: If no form with the given URL path exists
        ValueError: If the form has no draft to publish
    """
    form = db.session.query(FormDefinition).filter(FormDefinition.url_path == url_path).one()

    if not form.draft_json:
        raise ValueError(f"Form '{url_path}' has no draft to publish")

    form.published_json = form.draft_json
    form.published_at = datetime.now()
    form.updated_at = func.now()

    db.session.commit()
    return form
