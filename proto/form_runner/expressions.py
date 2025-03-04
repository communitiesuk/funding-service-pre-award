import ast
import datetime
import functools
import re
from collections import defaultdict
from typing import Any, Callable

import simpleeval

from db import db
from proto.common.data.models import (
    Fund,
    Organisation,
    ProtoDataCollectionDefinition,
    ProtoDataCollectionInstance,
    ProtoGrantRecipient,
    ProtoReportingRound,
    Round,
)
from proto.form_runner.helpers import get_answer_text_for_question_from_section_data


def serialize_collection_data(collection: ProtoDataCollectionInstance) -> dict[str, dict[str, Any]]:
    data = defaultdict(dict)

    for section in collection.section_data:
        for question in section.section.questions:
            data[section.section.slug.replace("-", "_")][question.slug.replace("-", "_")] = (
                get_answer_text_for_question_from_section_data(question, section)
            )

    return data


def deal_with_single_equals(expression):
    return re.sub(r"\b=[^=]", " == ", expression)


def build_context(this_collection: ProtoDataCollectionInstance | None = None, answer: Any | None = None):
    # It would be nice if "this collection"s data was somehow surfaced at the top-level, ie not namespaced, but
    # would need to give due consideration to namespace collisions. So I'm skipping that for now by having everything
    # namespaced.
    # I think it might be "nice" / "more usable" if the following stuff was available at the top-level:
    # - References to the questions in the "current" section
    # - References to sections in the "current" collection
    # - Then references to related objects, eg if we're doing monitoring, then the application, grant recipient, etc
    context = {}

    # Retrieve all of the related objects to inject as context, based on the data collection
    grant = (
        this_collection.application.round.proto_grant
        if this_collection and this_collection.application
        else this_collection.report.recipient.grant
        if this_collection and this_collection.report
        else None
    )
    if grant:
        context["grant"] = grant

    if this_collection:
        context["this_collection"] = serialize_collection_data(this_collection)

    application = (
        this_collection.application
        if this_collection and this_collection.application
        else this_collection.report.recipient.application
        if this_collection and this_collection.report
        else None
    )
    if application:
        context["application_round"] = application.round
        context["application"] = serialize_collection_data(application.data_collection_instance)

    recipient = this_collection.report.recipient if this_collection and this_collection.report else None
    if recipient:
        context["recipient"] = recipient
        context["organisation"] = recipient.organisation

    if this_collection and this_collection.report:
        context["reporting_round"] = this_collection.report.reporting_round
        context["reports"] = [
            serialize_collection_data(report.data_collection_instance)
            for report in this_collection.report.recipient.reports
        ]

    if answer is not None:
        context["answer"] = answer

    return context


def _autocomplete_context_for_collection_definition_data(definition: ProtoDataCollectionDefinition, prefix=""):
    data = []

    if not definition:
        return data

    if definition.sections:
        for section in definition.sections:
            if not section.questions:
                continue

            data.append(
                {
                    "value": prefix + section.slug.replace("-", "_") + ".",
                    "label": f"Questions for section '{section.title}'",
                }
            )

            for question in section.questions:
                data.append(
                    {
                        "value": prefix + section.slug.replace("-", "_") + "." + question.slug.replace("-", "_"),
                        "label": question.title,
                    }
                )

    return data


def _autocomplete_context_for_db_model(model: db.Model, prefix: str):
    data = []

    if hasattr(model, "context_fields"):
        for prop, description in model.context_fields.items():
            data.append({"value": prefix + prop, "label": description})

    else:
        for col in model.__table__.columns.keys():
            data.append({"value": prefix + col, "label": prefix + col})

    return data


def build_autocomplete_context(
    grant: Fund, this_definition: ProtoDataCollectionDefinition | None = None, answer: Any | None = None
):
    # All of this logic is very hacky so #donttrustme
    autocomplete_context = []

    # grant
    autocomplete_context.append({"value": "grant.", "label": "Metadata about the grant"})
    autocomplete_context.extend(_autocomplete_context_for_db_model(grant, prefix="grant."))

    # this_collection
    autocomplete_context.append({"value": "this_collection.", "label": "Information from this data collection"})
    autocomplete_context.extend(
        _autocomplete_context_for_collection_definition_data(this_definition, prefix="this_collection.")
    )

    # application_round
    autocomplete_context.append({"value": "application_round.", "label": "Metadata about the application round"})
    autocomplete_context.extend(_autocomplete_context_for_db_model(Round(), prefix="application_round."))

    # organisation
    autocomplete_context.append(
        {"value": "organisation.", "label": "Metadata about the grant recipient's organisation"}
    )
    autocomplete_context.extend(_autocomplete_context_for_db_model(Organisation(), prefix="organisation."))

    if grant.application_rounds and this_definition not in [
        ar.data_collection_definition for ar in grant.application_rounds
    ]:
        context_for_application = _autocomplete_context_for_collection_definition_data(
            grant.application_rounds[0].data_collection_definition, prefix="application."
        )
        if context_for_application:
            # application - skipping a lot of edge cases and considerations here
            autocomplete_context.append(
                {"value": "application.", "label": "Information from the original grant application"}
            )
            autocomplete_context.extend(context_for_application)

    if this_definition in [rr.data_collection_definition for rr in grant.reporting_rounds]:
        # grant recipient profile
        autocomplete_context.append({"value": "recipient.", "label": "Metadata about the grant recipient"})
        autocomplete_context.extend(_autocomplete_context_for_db_model(ProtoGrantRecipient(), prefix="recipient."))

        # reporting_round
        autocomplete_context.append({"value": "reporting_round.", "label": "Metadata about the reporting round"})
        autocomplete_context.extend(
            _autocomplete_context_for_db_model(ProtoReportingRound(), prefix="reporting_round.")
        )

        # reports
        for i, reporting_round in enumerate(grant.reporting_rounds):
            if this_definition is not reporting_round.data_collection_definition:
                context_for_reporting_round = _autocomplete_context_for_collection_definition_data(
                    reporting_round.data_collection_definition, prefix=f"reports[{i}]."
                )
                if context_for_reporting_round:
                    autocomplete_context.append(
                        {"value": f"reports[{i}].", "label": f"Information from monitoring report #{i + 1}"}
                    )
                    autocomplete_context.extend(context_for_reporting_round)

    if answer is not None:
        autocomplete_context.append({"value": "answer", "label": "The answer provided for this question"})

    # this shouldn't always be applied and should be nested but just doing this for now
    autocomplete_context.append({"value": "min", "label": "The minimum validation amount"})
    autocomplete_context.append({"value": "max", "label": "The maximum validation amount"})
    autocomplete_context.append({"value": "value", "label": "The validation amount"})
    return autocomplete_context


def build_context_injector(
    this_collection: ProtoDataCollectionInstance | None = None,
    answer: Any | None = None,
    additional_context: dict = {},  # noqa
) -> Callable[[str], str]:
    context = {**build_context(this_collection=this_collection, answer=answer), **additional_context}
    return functools.partial(interpolate, context=context)


def build_context_evaluator(
    this_collection: ProtoDataCollectionInstance | None = None,
    answer: Any | None = None,
    # smashing a nice clean abstraction, sorry - this could theoretically be built from the
    # data collection instance if you knew what question was relevant, maybe thats
    # how `answer` should be modelled too
    additional_context: dict = {},  # noqa
) -> Callable[[str], int | bool]:
    context = {**build_context(this_collection=this_collection, answer=answer), **additional_context}
    return functools.partial(evaluate, context=context)


def _restricted_evaluator(context):
    evaluator = simpleeval.EvalWithCompoundTypes(names=context, functions=dict(int=int, sum=sum))

    evaluator.nodes = {
        ast_expr: ast_fn
        for ast_expr, ast_fn in evaluator.nodes.items()
        if ast_expr
        in {
            ast.UnaryOp,
            ast.Expr,
            ast.Name,
            ast.BinOp,
            ast.BoolOp,
            ast.Compare,
            ast.Subscript,
            ast.Attribute,
            ast.Index,
            ast.Slice,
            ast.Constant,
            ast.Call,
        }
    }
    return evaluator


def _nicely_format(val):
    if isinstance(val, datetime.datetime):
        return val.strftime("%A %-d %B %Y")

    return str(val)


def interpolate(text: str, context: dict) -> str:
    evaluator = _restricted_evaluator(context)

    return re.sub(r"\(\((.*?)\)\)", lambda m: _nicely_format(evaluator.eval(m.group(1))), text)


def evaluate(text: str, context: dict) -> int | bool:
    evaluator = _restricted_evaluator(context)

    return evaluator.eval(text)
