from flask_wtf import FlaskForm
from wtforms import RadioField, TextAreaField
from wtforms.validators import InputRequired


class ApprovalForm(FlaskForm):
    pass


class ScoreForm(FlaskForm):
    """
    Given class is a form class model for scoring a sub-criteria fund
    """

    # for validation
    justification = TextAreaField("Justification", validators=[InputRequired()])


class OneToFiveScoreForm(ScoreForm):
    def __init__(self):
        ScoreForm.__init__(self)
        self.scores_list = [
            (5, "Strong"),
            (4, "Good"),
            (3, "Satisfactory"),
            (2, "Partial"),
            (1, "Poor"),
        ]
        self.max_score = 5

    # for validation
    score = RadioField("Score", choices=[1, 2, 3, 4, 5], validators=[InputRequired()])


class ZeroToThreeScoreForm(ScoreForm):
    def __init__(self):
        ScoreForm.__init__(self)
        self.scores_list = [
            (3, "Approved with feedback"),
            (2, "Approved with conditions"),
            (1, "Not approved"),
            (0, "Insufficient information provided"),
        ]
        self.max_score = 3

    # for validation
    score = RadioField("Score", choices=[0, 1, 2, 3], validators=[InputRequired()])


class ZeroToOneScoreForm(ScoreForm):
    def __init__(self):
        ScoreForm.__init__(self)
        self.scores_list = [
            (1, "Pass"),
            (0, "Fail"),
        ]
        self.max_score = 1

    # for validation
    score = RadioField("Score", choices=[0, 1], validators=[InputRequired()])


class ZeroToFourScoreForm(ScoreForm):
    def __init__(self):
        ScoreForm.__init__(self)
        self.scores_list = [
            (4, "Strong"),
            (3, "Good"),
            (2, "Satisfactory"),
            (1, "Partial"),
            (0, "Poor"),
        ]
        self.max_score = 4

    # for validation
    score = RadioField("Score", choices=[0, 1, 2, 3, 4], validators=[InputRequired()])
