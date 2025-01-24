from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovCheckboxesInput, GovSubmitInput, GovTextInput, GovRadioInput
from wtforms import SelectMultipleField, SubmitField, StringField, IntegerField, RadioField
from wtforms.validators import DataRequired, Regexp, Optional
from wtforms.widgets import HiddenInput

from proto.common.data.models import TemplateSection
from proto.common.data.models.question_bank import QuestionType


class ChooseTemplateSectionsForm(FlaskForm):
    sections = SelectMultipleField(
        _l("Choose templates from the question bank"),
        widget=GovCheckboxesInput(),
        validators=[],
    )
    submit = SubmitField(_l("Continue"), widget=GovSubmitInput())

    def __init__(self, template_sections: list[TemplateSection], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_sections = template_sections

        self.sections.choices = [(section.id, section.title) for section in self.template_sections]

    @property
    def section_questions(self):
        return [
            [question.title for question in template_section.template_questions]
            for template_section in self.template_sections
        ]


class NewSectionForm(FlaskForm):
    title = StringField(
        _l("What is name of the section?"),
        widget=GovTextInput(),
        validators=[DataRequired(message=_l("Enter the name of the section"))],
    )
    slug = StringField(
        _l("What is the URL slug for this section?"),
        widget=GovTextInput(),
        validators=[
            DataRequired(message=_l("Enter a URL slug for the section")),
            Regexp(r"[a-z\-]+", message=_l("Enter a URL slug using only letters and dashes")),
        ],
        filters=[lambda val: val.lower() if val else val],
    )
    order = IntegerField(
        widget=HiddenInput(),
    )
    submit = SubmitField(_l("Add section"), widget=GovSubmitInput())


class NewQuestionForm(FlaskForm):
    type = RadioField(
        _l("What type of question are you adding?"),
        widget=GovRadioInput(),
        choices=[(ft.value, ft.name) for ft in QuestionType],
        validators=[DataRequired(message=_l("Select a question type"))],
    )
    title = StringField(
        _l("What is the question?"),
        widget=GovTextInput(),
        validators=[DataRequired(message=_l("Enter the question"))],
    )
    hint = StringField(
        _l("What is the hint text for the question?"),
        description="Only provide this if additional information is needed to help answer the question correctly.",
        widget=GovTextInput(),
        validators=[Optional()],
    )
    slug = StringField(
        _l("What is the URL slug for this question?"),
        widget=GovTextInput(),
        validators=[
            DataRequired(message=_l("Enter a URL slug for the question")),
            Regexp(r"[a-z\-]+", message=_l("Enter a URL slug using only letters and dashes")),
        ],
    )
    order = IntegerField(
        widget=HiddenInput(),
    )
    submit = SubmitField(_l("Add question"), widget=GovSubmitInput())
