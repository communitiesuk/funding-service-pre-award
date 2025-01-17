from distutils.util import strtobool

from flask import abort, current_app, request

from assessment_store.db.queries.assessment_records.queries import (
    create_user_application_association,
    get_metadata_for_application,
    get_user_application_associations,
)
from assessment_store.db.queries.assessment_records.queries import (
    update_user_application_association as update_user_application_association_db,
)
from assessment_store.db.schemas.schemas import AllocationAssociationSchema
from assessment_store.services.data_services import (
    create_assessment_url_for_application,
    get_account_data,
    get_fund_data,
)
from common.blueprints import Blueprint
from services.notify import get_notification_service

assessment_user_bp = Blueprint("assessment_user_bp", __name__)


@assessment_user_bp.get("/application/<application_id>/users")
def get_all_users_associated_with_application(application_id):
    """Fetches all users associated with a given application.

    Parameters:
        application_id (str): UUID of the application.
        active (bool, optional): Filter for active associations. Defaults to None.

    Returns:
        list: Serialized list of user associations.

    Raises:
        404: If no users are found for the given application.

    """
    active = bool(strtobool(request.args.get("active"))) if "active" in request.args else None
    associations = get_user_application_associations(application_id=application_id, active=active)
    if associations:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(associations, many=True)

    current_app.logger.error(
        "Could not find any users associated with application %(application_id)s",
        dict(application_id=application_id),
    )
    abort(404)


@assessment_user_bp.get("/application/<application_id>/user/<user_id>")
def get_user_application_association(application_id, user_id):
    """Fetches the association between a given user and application.

    Parameters:
        application_id (str): UUID of the application.
        user_id (str): UUID of the user.

    Returns:
        dict: Serialized user application association.

    Raises:
        404: If no association is found between the user and the application.

    """
    association = get_user_application_associations(application_id=application_id, user_id=user_id)

    if association:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(association[0])

    current_app.logger.error(
        "Could not find association between %(user_id)s and application %(application_id)s",
        dict(user_id=user_id, application_id=application_id),
    )
    abort(404)


@assessment_user_bp.post("/application/<application_id>/user/<user_id>")
def add_user_application_association(application_id, user_id):
    """Creates a new association between a user and an application.

    Parameters:
        application_id (str): UUID of the application.
        user_id (str): UUID of the user.

    Returns:
        dict: Serialized new user application association.

    Raises:
        404: If the association cannot be created.

    """
    args = request.get_json()
    if "assigner_id" not in args:
        abort(400, "Post body must contain assigner_id field")

    send_email = args.get("send_email")
    assigner_id = args["assigner_id"]
    association = create_user_application_association(
        application_id=application_id, user_id=user_id, assigner_id=assigner_id
    )

    if association:
        if send_email:
            try:
                application = get_metadata_for_application(application_id)
                user_response = get_account_data(account_id=user_id)
                assigner_response = get_account_data(account_id=assigner_id)
                fund_response = get_fund_data(fund_id=application["fund_id"])
                get_notification_service().send_assessment_assigned_email(
                    email_address=user_response["email_address"],
                    reference_number=application["short_id"],
                    project_name=application["project_name"],
                    assignment_message=args.get("email_content"),
                    assessment_link=create_assessment_url_for_application(application_id=application_id),
                    lead_assessor_email=assigner_response["email_address"],
                    fund_name=fund_response["name"],
                )

            except Exception:
                current_app.logger.exception(
                    "Could not send assessment assigned email, user: {user_id}, application {application_id}",
                    extra=dict(user_id=user_id, application_id=application_id),
                )

        serialiser = AllocationAssociationSchema()
        return serialiser.dump(association), 201

    current_app.logger.error(
        "Could not create association between %(user_id)s and application %(application_id)s",
        dict(user_id=user_id, application_id=application_id),
    )
    abort(404)


@assessment_user_bp.put("/application/<application_id>/user/<user_id>")
def update_user_application_association(application_id, user_id):
    """Updates the active status of an association between a user and an
    application.

    Parameters:
        application_id (str): UUID of the application.
        user_id (str): UUID of the user.

    Returns:
        dict: Serialized updated user application association.

    Raises:
        400: If the 'active' parameter is missing in the request.
        404: If the association cannot be updated.

    """
    args = request.get_json()
    if "active" not in args:
        abort(400, "Body must contain active field")

    if "assigner_id" not in args:
        abort(400, "Post body must contain assigner_id field")

    send_email = args.get("send_email")
    active = args.get("active")
    assigner_id = args["assigner_id"]
    association = update_user_application_association_db(
        application_id=application_id,
        user_id=user_id,
        active=active,
        assigner_id=assigner_id,
    )

    if association:
        if send_email:
            try:
                application = get_metadata_for_application(application_id)
                user_response = get_account_data(account_id=user_id)
                assigner_response = get_account_data(account_id=assigner_id)
                fund_response = get_fund_data(fund_id=application["fund_id"])
                if active:
                    get_notification_service().send_assessment_assigned_email(
                        email_address=user_response["email_address"],
                        reference_number=application["short_id"],
                        project_name=application["project_name"],
                        assignment_message=args.get("email_content"),
                        assessment_link=create_assessment_url_for_application(application_id=application_id),
                        lead_assessor_email=assigner_response["email_address"],
                        fund_name=fund_response["name"],
                    )
                else:
                    get_notification_service().send_assessment_unassigned_email(
                        email_address=user_response["email_address"],
                        reference_number=application["short_id"],
                        project_name=application["project_name"],
                        assignment_message=args.get("email_content"),
                        assessment_link=create_assessment_url_for_application(application_id=application_id),
                        lead_assessor_email=assigner_response["email_address"],
                        fund_name=fund_response["name"],
                    )

            except Exception:
                current_app.logger.exception(
                    "Could not send assessment email, active: {active}, user: {user_id}, application {application_id}",
                    extra=dict(active=active, user_id=user_id, application_id=application["application_id"]),
                )

        serialiser = AllocationAssociationSchema()
        return serialiser.dump(association)

    current_app.logger.error(
        "Could not update association between %(user_id)s and application %(application_id)s",
        dict(user_id=user_id, application_id=application_id),
    )
    abort(404)


@assessment_user_bp.get("/user/<user_id>/applications")
def get_all_applications_associated_with_user(user_id, active=None):
    """Fetches all applications associated with a given user.

    Parameters:
        user_id (str): UUID of the user.
        active (bool, optional): Filter for active associations. Defaults to None.

    Returns:
        list: Serialized list of application associations.

    Raises:
        404: If no applications are found for the given user.

    """
    associations = get_user_application_associations(user_id=user_id, active=active)
    if associations:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(associations, many=True)

    current_app.logger.error("Could not find any applications associated with user %(user_id)s", dict(user_id=user_id))
    abort(404)


@assessment_user_bp.get("/user/<assigner_id>/assignees")
def get_all_associations_assigned_by_user(assigner_id, active=None):
    """Fetches all associations where the user is the assigner.

    Parameters:
        assigner_id (str): UUID of the assigner.
        active (bool, optional): Filter for active associations. Defaults to None.

    Returns:
        list: Serialized list of application associations.

    Raises:
        404: If no applications are found for the given user.

    """
    associations = get_user_application_associations(assigner_id=assigner_id, active=active)
    if associations:
        serialiser = AllocationAssociationSchema()
        return serialiser.dump(associations, many=True)

    current_app.logger.error(
        "Could not find any applications assigned by user %(assigner_id)s", dict(assigner_id=assigner_id)
    )
    abort(404)
