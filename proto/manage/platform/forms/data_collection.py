from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import (
    GovCheckboxesInput,
    GovRadioInput,
    GovSubmitInput,
    GovTextArea,
    GovTextInput,
)
from wtforms import IntegerField, RadioField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import HiddenInput

from proto.common.data.models import TemplateSection
from proto.common.data.models.question_bank import QuestionType, ValidationType


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


human_readable = {
    QuestionType.TEXT_INPUT: "Single line of text",
    QuestionType.TEXTAREA: "More than a single line of text",
    QuestionType.RADIOS: "Selection from a list of options",
    QuestionType.NUMBER: "Number",
    QuestionType.POUNDS_AND_PENCE: "Pounds and pence",
    QuestionType.LIST_AUTOCOMPLETE: "Selection from a list of options",
}


class NewQuestionTypeForm(FlaskForm):
    type = RadioField(
        _l("What type of question are you adding?"),
        widget=GovRadioInput(),
        choices=[(ft.value, human_readable.get(ft)) for ft in QuestionType if ft != QuestionType.RADIOS],
        coerce=lambda x: QuestionType(x).value,
        validators=[DataRequired(message=_l("Select a question type"))],
    )
    submit = SubmitField(_l("Continue"), widget=GovSubmitInput())


class NewConditionForm(FlaskForm):
    expression = StringField(
        _l("Expression"),
        widget=GovTextArea(),
        validators=[DataRequired(message=_l("Enter the expression"))],
    )
    submit = SubmitField(_l("Add condition"), widget=GovSubmitInput())


class SimpleNumberValidationForm(FlaskForm):
    type = RadioField(
        _l("The number should be:"),
        widget=GovRadioInput(),
        choices=[x.value for x in ValidationType],
        validators=[DataRequired(message=_l("Select which property should be valid"))],
    )
    min = IntegerField(_l("Minumum value"), widget=GovTextInput(), validators=[Optional()])
    max = IntegerField(_l("Maximum value"), widget=GovTextInput(), validators=[Optional()])
    value = IntegerField(_l("Value"), widget=GovTextInput(), validators=[Optional()])
    message = StringField(
        _l("Message"),
        widget=GovTextArea(),
        validators=[DataRequired(message=_l("Enter the message"))],
    )
    submit = SubmitField(_l("Add validation"), widget=GovSubmitInput())


class NewValidationForm(FlaskForm):
    expression = StringField(
        _l("Rule"),
        widget=GovTextArea(),
        validators=[DataRequired(message=_l("Enter the validation rule"))],
    )
    message = StringField(
        _l("Message"),
        widget=GovTextArea(),
        validators=[DataRequired(message=_l("Enter the message"))],
    )

    submit = SubmitField(_l("Add validation"), widget=GovSubmitInput())


class QuestionForm(FlaskForm):
    title = StringField(
        _l("Question text"),
        widget=GovTextArea(),
        validators=[DataRequired(message=_l("Enter the question text"))],
    )
    hint = StringField(
        _l("Hint text"),
        description="Only provide this if additional information is needed to help answer the question correctly.",
        widget=GovTextArea(),
        validators=[Optional()],
    )
    # mandatory = RadioField(
    #     _l("Is this question mandatory or optional?"),
    #     widget=GovRadioInput(),
    #     choices=[("mandatory", "Mandatory"), ("optional", "Optional")],
    #     render_kw={"items": [{}, {"hint": {"text": "We’ll add ‘(optional)’ to the end of the question text."}}]},
    # )
    order = IntegerField(
        widget=HiddenInput(),
    )
    type = StringField(
        widget=HiddenInput(),
    )

    submit = SubmitField(None, widget=GovSubmitInput())

    def __init__(self, *args, submit_label: str | None = _l("Add question"), **kwargs):
        super().__init__(*args, **kwargs)
        self.submit.label.text = submit_label
