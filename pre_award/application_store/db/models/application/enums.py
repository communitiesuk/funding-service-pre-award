from enum import Enum


class Language(Enum):
    en = 0
    cy = 1


class Status(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    SUBMITTED = 2
    COMPLETED = 3
    CHANGE_REQUESTED = 4
    CHANGE_RECEIVED = 5


class ApplicationsWithPiiDeleted(Enum):
    UN_SUBMITTED = "unsubmitted"
    ALL = "all"
