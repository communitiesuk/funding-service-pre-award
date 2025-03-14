from enum import Enum, auto


class ApplicationStatus(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    SUBMITTED = auto()
    CHANGE_REQUESTED = auto()
    CHANGE_RECEIVED = auto()
