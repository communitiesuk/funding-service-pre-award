from __future__ import annotations

import inspect
from dataclasses import dataclass


@dataclass
class Round:
    id: str = ""
    assessment_deadline: str = ""
    deadline: str = ""
    fund_id: str = ""
    opens: str = ""
    title: str = ""
    short_name: str = ""
    prospectus: str = ""
    instructions: str = ""
    contact_email: str = ""
    application_guidance: str = ""
    is_expression_of_interest: bool = False
    has_eligibility: bool = False

    @classmethod
    def from_dict(cls, d: dict):
        # Filter unknown fields from JSON dictionary
        return cls(
            **{k: v for k, v in d.items() if k in inspect.signature(cls).parameters},
            has_eligibility=d["eligibility_config"]["has_eligibility"],
        )
