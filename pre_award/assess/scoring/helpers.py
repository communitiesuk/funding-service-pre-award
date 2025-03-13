from flask import abort, current_app

from pre_award.assess.scoring.forms.scores_and_justifications import (
    OneToFiveScoreForm,
    ZeroToFourScoreForm,
    ZeroToOneScoreForm,
    ZeroToThreeScoreForm,
)
from pre_award.assess.services.data_services import get_scoring_system  # noqa


def get_scoring_class(round_id):
    scoring_system = get_scoring_system(round_id)

    try:
        class_mapping = {
            "ZeroToThree": ZeroToThreeScoreForm,
            "OneToFive": OneToFiveScoreForm,
            "ZeroToOne": ZeroToOneScoreForm,
            "ZeroToFour": ZeroToFourScoreForm,
        }
        scoring_form_class = class_mapping[scoring_system]
    except KeyError:
        current_app.logger.error("Scoring system '%(scoring_system)s' not found.", dict(scoring_system=scoring_system))
        abort(
            500,
            description=f"Scoring system '{scoring_system}' for round {round_id} has not been configured.",
        )
    return scoring_form_class
