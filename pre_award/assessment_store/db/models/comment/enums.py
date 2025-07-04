from enum import Enum


class CommentType(Enum):
    """Status The ENUM used by `db.models.Comments` to validate the possible
    values for the `comment_type` column."""

    COMMENT = 0
    WHOLE_APPLICATION = 1

    @property
    def label(self):
        if self == CommentType.WHOLE_APPLICATION:
            return "Application-level comment"
        elif self == CommentType.COMMENT:
            return "Sub-criteria comment"
