from enum import Enum


class ScoringSystem(Enum):
    """The ENUM used by `db.models.AssessmentRound` to validate the possible
    values for the `scoring_system` column."""

    OneToFive = 0
    ZeroToThree = 1
    ZeroToOne = 2
