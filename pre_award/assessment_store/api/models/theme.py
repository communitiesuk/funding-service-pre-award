import inspect
from dataclasses import dataclass
from typing import List

from dataclass_dict_convert import dataclass_dict_convert

from assessment_store.api.models.answer import Answer


@dataclass_dict_convert()
@dataclass()
class Theme:
    id: str
    name: str
    answers: List[Answer]

    def __post_init__(self):
        self.answers = [Answer.from_filtered_dict(answer) for answer in self.answers]

    @classmethod
    def from_filtered_dict(cls, d: dict):
        # Filter unknown fields from JSON dictionary
        return cls(**{k: v for k, v in d.items() if k in inspect.signature(cls).parameters})
