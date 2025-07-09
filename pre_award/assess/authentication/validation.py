import functools
from collections import defaultdict
from functools import wraps
from typing import Callable, List, Mapping, Sequence

from flask import abort, g
from fsd_utils.authentication.decorators import login_required

from pre_award.assess.assessments.models.round_status import RoundStatus, determine_round_status
from pre_award.assess.assessments.status import is_score_or_change_request_allowed_uncompeted
from pre_award.assess.services.data_services import get_application_metadata, get_fund, get_round, is_uncompeted_flow
from pre_award.assess.services.shared_data_helpers import get_state_for_tasklist_banner
from pre_award.assess.shared.helpers import get_ttl_hash, get_value_from_request
from pre_award.config import Config

_UK_COUNTRIES: list[str] = [
    "ENGLAND",
    "SCOTLAND",
    "WALES",
    "NORTHERNIRELAND",  # normalise locations
]

_ROLES: list[str] = [
    "LEAD_ASSESSOR",
    "ASSESSOR",
    "COMMENTER",
]

_HAS_DEVOLVED_AUTHORITY_VALIDATION: Mapping[str, bool] = defaultdict(
    lambda *_: False,  # by default, no devolved authority validation
    {
        "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4": True,
        "cof": True,
    },  # a dict of fund_round_id: bool, this could eventually be moved to fund store
)


def _get_access_roles(fund_short_name: str) -> frozenset[str]:
    return frozenset(f"{fund_short_name}_{role}".casefold() for role in _ROLES)


def _normalise_country(country: str) -> str:
    country = country.casefold()
    if country in {c.casefold() for c in _UK_COUNTRIES}:
        return country
    if country in ("ni", "northern ireland"):
        return "NORTHERNIRELAND".casefold()
    return country


def _get_all_country_roles(short_name: str) -> frozenset[str]:
    return frozenset(f"{short_name}_{c}".casefold() for c in _UK_COUNTRIES)


def _get_all_users_roles() -> frozenset[str]:
    return frozenset(r.casefold() for r in g.user.roles)


def get_valid_country_roles(short_name: str) -> frozenset[str]:
    all_roles = _get_all_users_roles()
    country_roles = _get_all_country_roles(short_name)
    return frozenset(all_roles.intersection(country_roles))


def get_countries_from_roles(short_name: str) -> frozenset[str]:
    valid_country_roles = get_valid_country_roles(short_name)
    partitioned_country_roles = (vcr.partition("_") for vcr in valid_country_roles)
    return frozenset(country for _, _, country in partitioned_country_roles)


def has_relevant_country_role(country: str, short_name: str) -> bool:
    return f"{short_name}_{country}".casefold() in _get_all_users_roles()


def _get_roles_by_fund_short_name(short_name: str, roles: Sequence[str]) -> list[str]:
    return [f"{short_name.upper()}_{role.upper()}" for role in roles]


def has_devolved_authority_validation(*, fund_id: str = None, short_name: str = None) -> bool:
    identifier = fund_id or short_name
    if not identifier:
        return False
    identifier = identifier.casefold()
    return _HAS_DEVOLVED_AUTHORITY_VALIDATION[identifier]


def has_access_to_fund(short_name: str) -> bool:
    all_roles = _get_all_users_roles()
    access_roles = _get_access_roles(short_name)
    return any(role in all_roles for role in access_roles)


def check_access_application_id(func: Callable = None, roles_required: List[str] | None = None) -> Callable:
    if roles_required is None:
        roles_required = []
    if func is None:
        return lambda f: check_access_application_id(func=f, roles_required=roles_required)

    @wraps(func)
    def decorated_function(*args, **kwargs):
        application_id = get_value_from_request(
            (
                "application_id",
                "application",
            )
        )
        if not application_id:
            abort(404)

        application_metadata = get_application_metadata(application_id)
        short_name = get_fund(
            application_metadata["fund_id"],
            ttl_hash=get_ttl_hash(Config.LRU_CACHE_TIME),
        ).short_name

        round_status: RoundStatus = determine_round_status(
            fund_id=application_metadata["fund_id"],
            round_id=application_metadata["round_id"],
        )
        if not round_status.has_assessment_opened:
            abort(403, "This assessment is not yet live.")

        if not has_access_to_fund(short_name):
            abort(403)

        fund_roles_required = _get_roles_by_fund_short_name(short_name, roles_required)
        login_required_function = login_required(func, roles_required=fund_roles_required)

        if has_devolved_authority_validation(fund_id=application_metadata["fund_id"]):
            if country := application_metadata.get("location_json_blob", {}).get("country"):
                if not has_relevant_country_role(_normalise_country(country), short_name):
                    abort(403)

        g.access_controller = AssessmentAccessController(short_name)
        return login_required_function(*args, **kwargs)

    return decorated_function


def _check_access_fund_common(
    func: Callable = None,
    roles_required: List[str] | None = None,
    fund_key: str = "fund_short_name",
    round_key: str = "round_short_name",
) -> Callable:
    if roles_required is None:
        roles_required = []
    if func is None:  # if used as a partial function
        return lambda f: _check_access_fund_common(
            func=f,
            roles_required=roles_required,
            fund_key=fund_key,
            round_key=round_key,
        )

    @wraps(func)
    def decorated_function(*args, **kwargs):
        fund_value = get_value_from_request((fund_key,))
        round_value = get_value_from_request((round_key,))
        if not fund_value:
            abort(404)

        using_short_name = fund_key == "fund_short_name"

        short_name = (
            fund_value
            if using_short_name
            else get_fund(fund_value, ttl_hash=get_ttl_hash(Config.LRU_CACHE_TIME)).short_name
        )

        round_details = get_round(fund_value, round_value, using_short_name)
        round_status: RoundStatus = determine_round_status(round=round_details)
        if not round_status.has_assessment_opened:
            abort(403, "This assessment is not yet live.")

        fund_roles_required = _get_roles_by_fund_short_name(short_name, roles_required)
        login_required_function = login_required(func, roles_required=fund_roles_required)

        if not has_access_to_fund(short_name):
            abort(403)

        g.access_controller = AssessmentAccessController(short_name)
        return login_required_function(*args, **kwargs)

    return decorated_function


check_access_fund_id_round_id = functools.partial(_check_access_fund_common, fund_key="fund_id", round_key="round_id")
check_access_fund_short_name_round_sn = functools.partial(
    _check_access_fund_common,
    fund_key="fund_short_name",
    round_key="round_short_name",
)


def check_approval_or_change_request_allowed_uncompeted_only(func):
    """
    Decorator to enforce access control for endpoints related to scoring and requesting changes
    in the context of 'uncompeted' fund flows.

    This decorator checks whether the current application and sub-criteria are eligible for
    scoring or change requests based on the application's state and fund type. If the fund is
    part of an uncompeted flow and there are pending change requests, access is denied with a
    context-specific 403 error message.

    The error message varies depending on the endpoint being accessed:
    - For 'request_changes': informs that changes cannot be requested due to pending requests.
    - For 'score': informs that scoring is blocked due to pending change requests.
    - For other endpoints: provides a generic access denial message.

    Args:
        func (Callable): The view function to wrap.

    Returns:
        Callable: The wrapped function with access control applied.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        application_id = kwargs.get("application_id") or get_value_from_request(("application_id",))
        sub_criteria_id = kwargs.get("sub_criteria_id") or get_value_from_request(("sub_criteria_id",))

        if not application_id or not sub_criteria_id:
            abort(400, "Missing application or sub-criteria ID.")

        state = get_state_for_tasklist_banner(application_id)
        fund_id = state.fund_id if hasattr(state, "fund_id") else get_application_metadata(application_id)["fund_id"]

        if is_uncompeted_flow(fund_id):
            if not is_score_or_change_request_allowed_uncompeted(state, sub_criteria_id):
                if func.__name__ == "request_changes":
                    abort(403, "You cannot request changes when there are still pending change requests.")
                elif func.__name__ == "score":
                    abort(403, "Scoring is not allowed when there are still pending change requests.")
                else:
                    abort(403, "Action not allowed for this application at this stage.")

        return func(*args, **kwargs)

    return wrapper


class AssessmentAccessController(object):
    def __init__(self, fund_short_name: str = None):
        self.fund_short_name = fund_short_name

    @property
    def is_lead_assessor(self) -> bool:
        return f"{self.fund_short_name}_LEAD_ASSESSOR" in g.user.roles

    @property
    def is_assessor(self) -> bool:
        return f"{self.fund_short_name}_ASSESSOR" in g.user.roles

    @property
    def is_commenter(self) -> bool:
        return f"{self.fund_short_name}_COMMENTER" in g.user.roles

    @property
    def has_any_assessor_role(self) -> bool:
        return self.is_lead_assessor or self.is_assessor
