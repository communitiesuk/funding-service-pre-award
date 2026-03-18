# Using RETENTION_ALREADY_EXPIRED for rounds where the unsubmitted retention
# deadline has already passed, these will be immediately eligible for deletion
RETENTION_ALREADY_EXPIRED = 0

# Using default value Applied when a round is not in ROUND_RETENTION,
# or when submitted_days / unsubmitted_days is None and not yet confirmed.

DEFAULT_SUBMITTED_DAYS = 6 * 365  # 6 years
DEFAULT_UNSUBMITTED_DAYS = 1 * 365  # 1 year

ROUND_RETENTION = {
    "COF-R2W2": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": RETENTION_ALREADY_EXPIRED,
        "source": "privacy_notice",
    },
    "COF-R2W3": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": RETENTION_ALREADY_EXPIRED,
        "source": "privacy_notice",
    },
    "COF-R3W1": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": RETENTION_ALREADY_EXPIRED,
        "source": "privacy_notice",
    },
    "COF-R3W2": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": RETENTION_ALREADY_EXPIRED,
        "source": "privacy_notice",
    },
    "COF-R3W3": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": RETENTION_ALREADY_EXPIRED,
        "source": "privacy_notice",
    },
    "COF-R4W1": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": RETENTION_ALREADY_EXPIRED,
        "source": "privacy_notice",
    },
    "COF-R4W2": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": RETENTION_ALREADY_EXPIRED,
        "source": "privacy_notice",
    },
    "COF-EOI-R1": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": RETENTION_ALREADY_EXPIRED,
        "source": "privacy_notice",
    },
    "CHAM-APPLY": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": 6 * 30,
        "source": "privacy_notice",
    },
    "CHAM-REG": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": 6 * 30,
        "source": "privacy_notice",
    },
    "CFA-R1": {
        "submitted_days": 2 * 365,
        "unsubmitted_days": 1 * 365,
        "source": "privacy_notice",
    },
    "CYP-R1": {
        "submitted_days": 10 * 365,
        "unsubmitted_days": RETENTION_ALREADY_EXPIRED,
        "source": "privacy_notice",
    },
    "DPIF-R2": {
        "submitted_days": 2 * 365,
        "unsubmitted_days": 1 * 365,
        "source": "privacy_notice",
    },
    "DPIF-R3": {
        "submitted_days": 2 * 365,
        "unsubmitted_days": 1 * 365,
        "source": "privacy_notice",
    },
    "DPIF-R4": {
        "submitted_days": 2 * 365,
        "unsubmitted_days": 1 * 365,
        "source": "privacy_notice",
    },
    "GBRF-R1": {
        "submitted_days": 2 * 365,
        "unsubmitted_days": 1 * 365,
        "source": "privacy_notice",
    },
    "HSRA-RP": {
        "submitted_days": 10 * 365,
        "unsubmitted_days": 1 * 365,
        "source": "privacy_notice",
    },
    "HSRA-VR": {
        "submitted_days": 10 * 365,
        "unsubmitted_days": 1 * 365,
        "source": "privacy_notice",
    },
    "LPDF-R1": {
        "submitted_days": 2 * 365,
        "unsubmitted_days": 1 * 365,
        "source": "privacy_notice",
    },
    "LPDF-R2": {
        "submitted_days": 2 * 365,
        "unsubmitted_days": 1 * 365,
        "source": "privacy_notice",
    },
    "NSTF-R2": {
        "submitted_days": 2 * 365,
        "unsubmitted_days": RETENTION_ALREADY_EXPIRED,
        "source": "privacy_notice",
    },
    "PFN-RP": {
        "submitted_days": 7 * 365,
        "unsubmitted_days": 1 * 365,
        "source": "privacy_notice",
    },
    "SHIF-APPLY": {
        "submitted_days": 3 * 365,
        "unsubmitted_days": 6 * 30,
        "source": "privacy_notice",
    },
    "EHCF-APPLY": {
        "submitted_days": None,
        "unsubmitted_days": None,
        "source": "not_documented",
    },
    "LAHF-LAHFtu": {
        "submitted_days": None,
        "unsubmitted_days": None,
        "source": "not_documented",
    },
    "NWP-PILL1": {
        "submitted_days": None,
        "unsubmitted_days": None,
        "source": "not_documented",
    },
    "NWP-PILL2": {
        "submitted_days": None,
        "unsubmitted_days": None,
        "source": "not_documented",
    },
    "NWP-PILL3": {
        "submitted_days": None,
        "unsubmitted_days": None,
        "source": "not_documented",
    },
    "NWP-PILL4": {
        "submitted_days": None,
        "unsubmitted_days": None,
        "source": "not_documented",
    },
}


def get_retention_config(fund_short_name: str, round_short_name: str) -> tuple[int, int, str]:
    """
    Returns (submitted_days, unsubmitted_days, source) for a given fund/round.

    Args:
        fund_short_name:  Fund.short_name from DB  e.g. "COF"
        round_short_name: Round.short_name from DB e.g. "R2W2"

    Usage:
        submitted_days, unsubmitted_days, source = get_retention_config("COF", "R2W2")
    """
    key = f"{fund_short_name}-{round_short_name}"
    config = ROUND_RETENTION.get(key)

    if config and config["submitted_days"] is not None:
        return (
            config["submitted_days"],
            config["unsubmitted_days"],
            config["source"],
        )

    return DEFAULT_SUBMITTED_DAYS, DEFAULT_UNSUBMITTED_DAYS, "default_applied"
