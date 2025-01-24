from enum import Enum


class Status(Enum):
    """Status The ENUM used by `db.models.AssessmentRecord` to validate the
    possible values for the `workflow_status` column."""

    NOT_STARTED = 0
    IN_PROGRESS = 1
    SUBMITTED = 2
    COMPLETED = 3
    CHANGE_REQUESTED = 4
    CHANGE_RECEIVED = 5


class Language(Enum):
    """Status The ENUM used by `db.models.AssessmentRecord` to validate the
    possible values for the `language` column."""

    en = 0
    cy = 1
