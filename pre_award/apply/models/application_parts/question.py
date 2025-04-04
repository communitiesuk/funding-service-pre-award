from dataclasses import dataclass
from typing import List

from pre_award.apply.models.application_parts.field import Field


@dataclass
class Question:
    question: str
    status: str
    fields: List[Field]
