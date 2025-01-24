from dataclasses import dataclass
from typing import List

from pre_award.apply.models.application_parts.question import Question


@dataclass
class Form:
    name: str
    status: str
    questions: List[Question]
    metadata: str
