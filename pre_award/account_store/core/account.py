"""
Contains the functions directly used by the openapi spec.
"""

from typing import Dict, Tuple

import sqlalchemy
from email_validator import validate_email
from flask import abort, request
from sqlalchemy import any_, delete, or_, select
from sqlalchemy.orm import selectinload

from pre_award.account_store.db.models.account import Account
from pre_award.account_store.db.models.role import Role
from pre_award.account_store.db.schemas.account import AccountSchema
from pre_award.common.blueprints import Blueprint
from pre_award.db import db

account_core_bp = Blueprint("account_core_bp", __name__)


@account_core_bp.get("/accounts")
def get_account() -> Tuple[dict, int]:
    """
    Get a single account corresponding to the given unique parameters
    and return account object schema and status code
    :param account_id: (str) the id to search
    :param email_address: (str) the email to search
    :param azure_ad_subject_id: (str) the azure_ad_subject_id to search
    :return:
        Tuple of account object (or error) dict and status int
    """
    account_id = request.args.get("account_id")
    email_address = request.args.get("email_address")
    azure_ad_subject_id = request.args.get("azure_ad_subject_id")
    if not any([account_id, email_address, azure_ad_subject_id]):
        return {
            "error": (
                "Bad request: please provide at least 1 query argument of "
                "account_id, email_address or azure_ad_subject_id"
            )
        }, 400

    stmnt = select(Account)
    email_address = email_address.lower() if email_address else email_address

    if account_id:
        stmnt = stmnt.filter(Account.id == account_id)
    if email_address:
        stmnt = stmnt.filter(Account.email == email_address)
    if azure_ad_subject_id:
        stmnt = stmnt.filter(Account.azure_ad_subject_id == azure_ad_subject_id)

    try:
        result = db.session.execute(stmnt)
        account = result.scalars().one()
        account_schema = AccountSchema()
        return account_schema.dump(account), 200
    except sqlalchemy.exc.NoResultFound:
        return {"error": "No matching account found"}, 404


@account_core_bp.get("/bulk-accounts")
def get_bulk_accounts() -> Dict:
    """
    Get multiple accounts corresponding to the given account ids
    and return account object schema and status code
    :param account_id: List of ids to search
    :return:
        Nested dict of account_id: {account object}
    """
    raw_account_id = request.args.getlist("account_id")

    # Filter out any empty/blank strings like '', which could happen with eg `?account_id=`
    account_id = [account_id for account_id in raw_account_id if account_id]
    if not account_id:
        return {"error": "Bad request: please provide at least 1 account_id "}, 400

    stmnt = select(Account)
    stmnt = stmnt.filter(Account.id.in_(account_id))

    try:
        result = db.session.scalars(stmnt)
        account_schema = AccountSchema()

        accounts_metadatas = {str(account_row.id): account_schema.dump(account_row) for account_row in result}

        return accounts_metadatas, 200
    except sqlalchemy.exc.NoResultFound:
        return {"error": "No matching account found"}, 404


@account_core_bp.put("/accounts/<string:account_id>")
def put_account(account_id: str) -> Tuple[dict, int]:
    """put_account Given an account id and a role,
    if the account_id exists in the db the corresponding
    entry in the db is updated with the corresponding role.

    Args:
        account_id (str, required): An account_id given as a string.
    Json Args:
        roles (str, required): An array of roles given as a string.
        azure_ad_subject_id (str, required): Subject id of the Azure AD object.
        email (str, optional): Preferred email of the account holder.
        full_name (str, optional): First and last name given as a string.
        Defaults to None.

    Returns:
        dict, int
    """
    # Validate request body
    try:
        roles = request.json["roles"]
    except KeyError:
        return {"detail": "roles are required"}, 400
    try:
        azure_ad_subject_id = request.json["azure_ad_subject_id"]
    except KeyError:
        return {"detail": "'azure_ad_subject_id' is a required property"}, 400

    full_name = request.json.get("full_name")
    email = request.json.get("email_address", "").lower()

    # Check account exists
    try:
        account = (
            db.session.query(Account)
            .filter(
                Account.id == account_id,
                or_(
                    Account.azure_ad_subject_id == azure_ad_subject_id,
                    Account.azure_ad_subject_id.is_(None),
                ),
            )
            .one()
        )
    except sqlalchemy.exc.NoResultFound:
        return {"error": "No account matching those details could be found"}, 404

    # Delete existing roles
    stmnt = delete(Role).where(Role.account_id == account_id)
    db.session.execute(stmnt)

    if email:
        try:
            account.email = email
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.flush()
            db.session.rollback()
            return {
                "error": "Email cannot be updated - another account may already be using this email",
                "domain": parse_domain(email),
            }, 401
    if full_name:
        account.full_name = full_name
    if azure_ad_subject_id:
        account.azure_ad_subject_id = azure_ad_subject_id

    # Update current roles
    current_roles = []
    for role in roles:
        current_role = Role()
        current_role.account_id = account_id
        current_role.role = role.upper()
        current_roles.append(current_role)

    db.session.add_all(current_roles)

    db.session.commit()

    get_account_stmnt = select(Account).filter(Account.id == account_id)

    result = db.session.execute(get_account_stmnt)
    account = result.scalars().one()
    account_schema = AccountSchema()

    return account_schema.dump(account), 201


def parse_domain(email: str):
    try:
        parsed = validate_email(email, check_deliverability=False)
        return parsed.domain
    except Exception:
        return None


@account_core_bp.post("/accounts")
def post_account() -> Tuple[dict, int]:
    """
    Creates a new account in the db, given an email (required)
    and optional azure_ad_subject_id.

    If an account with this email address already exists then a 409
    is returned, otherwise a 201 is returned.

    Json Args:
        email_address (str, required): An valid email given as a string.
        azure_ad_subject_id (str, optional):
            An Azure AD subject ID given as a string.

    Returns:
        Returns a dictionary(json) along with a status code.
    """
    email_address = request.json.get("email_address", "").lower()
    azure_ad_subject_id = request.json.get("azure_ad_subject_id")
    if not email_address:
        return {"error": "email_address is required"}, 400
    try:
        new_account = Account(email=email_address, azure_ad_subject_id=azure_ad_subject_id)
        db.session.add(new_account)
        db.session.commit()
        new_account_json = {
            "account_id": new_account.id,
            "email_address": email_address,
            "azure_ad_subject_id": azure_ad_subject_id,
        }
        return new_account_json, 201
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return (
            "An account with that email or azure_ad_subject_id already exists",
            409,
        )


@account_core_bp.get("/accounts/fund/<string:fund_short_name>")
def get_accounts_for_fund(fund_short_name: str):
    include_assessors = True if request.args.get("include_assessors", "true").lower() == "true" else False
    include_commenters = True if request.args.get("include_commenters", "true").lower() == "true" else False
    round_short_name = request.args.get("round_short_name")
    if not include_assessors and not include_commenters:
        return {"error": "One of include_assessors or include_commenters must be true"}, 400
    query = (
        db.session.query(Account)
        .join(Role)  # Explicitly join the tables
        .filter(Role.role.like(f"%{fund_short_name}%"))  # Filter based on the Role attribute
        .options(selectinload(Account.roles))
    )
    if round_short_name:
        query = query.filter(Role.role.like(f"%{round_short_name}%"))

    if include_commenters and not include_assessors:
        query = query.filter(Role.role.like("%COMMENTER%"))
    elif include_assessors and not include_commenters:
        query = query.filter(Role.role.like("%ASSESSOR%"))
    else:
        query = query.filter(or_(Role.role.like("%ASSESSOR%"), Role.role.like("%COMMENTER%")))

    results = query.all()
    if not results:
        return {"error": "No matching accounts found"}, 404

    account_schema = AccountSchema()
    return account_schema.dump(results, many=True), 200


@account_core_bp.post("/accounts/search")
def search_accounts():
    body = request.json if request.content_type == "application/json" else {}
    email_domain = body.get("email_domain", None)
    roles = body.get("roles", list())
    partial_roles = body.get("partial_roles", list())

    if roles and partial_roles:
        abort(400)

    query = db.session.query(Account).join(Role).options(selectinload(Account.roles))

    if email_domain:
        query = query.filter(Account.email.ilike(f"%@{email_domain}"))

    if roles:
        query = query.filter(Role.role.like(any_(roles)))

    elif partial_roles:
        wildcard_partial_roles = ["%" + partial_role + "%" for partial_role in partial_roles]
        query = query.filter(Role.role.like(any_(wildcard_partial_roles)))

    account_schema = AccountSchema()
    return account_schema.dump(query.order_by(Account.email).all(), many=True), 200
