from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovCheckboxesInput, GovRadioInput, GovSubmitInput, GovTextInput
from wtforms import IntegerField, RadioField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional
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
    order = IntegerField(
        widget=HiddenInput(),
    )
    submit = SubmitField(_l("Add question"), widget=GovSubmitInput())
