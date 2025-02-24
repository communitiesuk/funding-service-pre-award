import ast
import functools
import re
from collections import defaultdict
from typing import Any, Callable

import simpleeval

from proto.common.data.models import (
    ProtoDataCollectionInstance,
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


def build_context(
    this_collection: ProtoDataCollectionInstance | None = None,
    answer: Any | None = None,
):
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
        if this_collection.application
        else this_collection.report.recipient.grant
        if this_collection.report
        else None
    )
    if grant:
        context["grant"] = grant

    if this_collection:
        context["this_collection"] = serialize_collection_data(this_collection)

    application = (
        this_collection.application
        if this_collection.application
        else this_collection.report.recipient.application
        if this_collection.report
        else None
    )
    if application:
        context["application"] = serialize_collection_data(application.data_collection_instance)

    recipient = this_collection.report.recipient if this_collection.report else None
    if recipient:
        context["recipient"] = recipient

    reports = this_collection.report.recipient.reports if this_collection.report else None
    if reports:
        context["reports"] = [serialize_collection_data(report.data_collection_instance) for report in reports]

    if answer:
        context["answer"] = answer

    return context


def build_context_injector(
    this_collection: ProtoDataCollectionInstance | None = None,
) -> Callable[[str], str]:
    context = build_context(this_collection=this_collection)
    return functools.partial(interpolate, context=context)


def build_context_evaluator(
    this_collection: ProtoDataCollectionInstance | None = None,
    answer: Any | None = None,
) -> Callable[[str], int | bool]:
    context = build_context(this_collection=this_collection, answer=answer)
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


def interpolate(text: str, context: dict) -> str:
    evaluator = _restricted_evaluator(context)

    return re.sub(r"\(\((.*?)\)\)", lambda m: str(evaluator.eval(m.group(1))), text)


def evaluate(text: str, context: dict) -> int | bool:
    evaluator = _restricted_evaluator(context)

    return evaluator.eval(text)
