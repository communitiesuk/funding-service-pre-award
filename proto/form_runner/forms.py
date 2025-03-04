from functools import partial

from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from govuk_frontend_wtf.wtforms_widgets import GovRadioInput, GovSelect, GovSubmitInput, GovTextArea, GovTextInput
from markupsafe import Markup
from wtforms.fields.choices import RadioField, SelectField
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from proto.common.data.models import (
    ProtoDataCollectionDefinitionQuestion,
    ProtoDataCollectionInstance,
)
from proto.common.data.models.question_bank import QuestionType
from proto.common.data.services.applications import get_current_answer_to_question
from proto.form_runner.expressions import build_context_evaluator, build_context_injector
from proto.form_runner.helpers import get_answer_value_for_question


# Build the form class and attach a field for it that renders the question correctly.
class DynamicQuestionForm(FlaskForm):
    submit = SubmitField(_l("Continue"), widget=GovSubmitInput())
    question: StringField | RadioField


# this will take the question type to add default type validators like is valid date
def build_validators(
    question: ProtoDataCollectionDefinitionQuestion, data_collection_instance: "ProtoDataCollectionInstance"
):
    validators = []

    # if question.required:
    validators.append(InputRequired())

    for validation in question.validations:
        # doesn't think about interpolating answers into the validation message but that could very neatly
        # follow the `build_context_injector` methodology below
        def custom_validator(validation, form, field):
            # note field.data won't be populated if the data was erroneous (a string for
            # a number field) it should know what to do with that
            # assuming each of the expressions needs the data to be well formed and
            # coerced lets skip for now
            if field.process_errors:
                return

            if validation.depends_on_question:
                section = next(
                    x
                    for x in data_collection_instance.section_data
                    if x.section.id == validation.depends_on_question.section.id
                )
                answer = get_answer_value_for_question(
                    question=validation.depends_on_question,
                    answer_data=section.data.get(validation.depends_on_question),
                )
            else:
                # there are edge cases here where the field answer from the input
                # needs to be transformed based on the question type before
                # it can be evaulated - we don't think about that too early on
                answer = field.data

            context_evaluator = build_context_evaluator(
                this_collection=data_collection_instance, answer=answer, additional_context=validation.options
            )
            context_injector = build_context_injector(
                this_collection=data_collection_instance, answer=answer, additional_context=validation.options
            )
            if not context_evaluator(validation.expression):
                raise ValidationError(context_injector(validation.message))

        validators.append(partial(custom_validator, validation))
    return validators


def build_question_form(
    data_collection_instance: ProtoDataCollectionInstance,
    question: ProtoDataCollectionDefinitionQuestion,
    context_injector,
) -> DynamicQuestionForm:
    question_text = context_injector(question.title)
    question_hint = Markup(context_injector(question.hint)) if question.hint else ""
    validators = build_validators(question, data_collection_instance)

    match question.type:
        case QuestionType.TEXT_INPUT:
            field = StringField(
                label=question_text, description=question_hint, widget=GovTextInput(), validators=validators
            )
        case QuestionType.TEXTAREA:
            field = StringField(
                label=question_text,
                description=question_hint,
                widget=GovTextArea(),
                validators=validators,
            )
        case QuestionType.RADIOS:
            field = RadioField(
                label=question_text,
                description=question_hint,
                choices=[(choice["value"], choice["label"]) for choice in question.data_source],
                widget=GovRadioInput(),
                validators=validators,
            )
        case QuestionType.NUMBER:
            # keep it simple and whole numbers for now, there is a decimal field but we'll
            # see what the differences are
            field = IntegerField(
                label=question_text, description=question_hint, widget=GovTextInput(), validators=validators
            )
        case QuestionType.POUNDS_AND_PENCE:
            field = FloatField(
                label=question_text, description=question_hint, widget=GovTextInput(), validators=validators
            )
        case QuestionType.LIST_AUTOCOMPLETE:
            field = SelectField(
                label=question_text,
                description=question_hint,
                widget=GovSelect(),
                validators=validators,
                choices=[(choice.value, choice.label) for choice in question.reference_data_source.data],
            )
        case _:
            raise Exception("Unable to generate dynamic form for question type {_}")

    DynamicQuestionForm.question = field

    # Populate form with existing answer (if any) from the DB
    form = DynamicQuestionForm(
        data={
            "question": get_answer_value_for_question(
                question, get_current_answer_to_question(data_collection_instance, question)
            )
        }
    )

    return form


class MarkAsCompleteForm(FlaskForm):
    complete = RadioField(
        _l("Do you want to mark this section as complete?"),
        choices=(("yes", "Yes"), ("no", "No")),
        coerce=lambda x: x == "yes",
        widget=GovRadioInput(),
        validators=[InputRequired(message="Choose yes if your answers are all complete")],
    )
    submit = SubmitField(_l("Save and continue"), widget=GovSubmitInput())
