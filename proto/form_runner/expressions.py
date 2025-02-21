import ast
import functools
import re
from collections import defaultdict
from typing import Any, Callable

import simpleeval

from proto.common.data.models import ProtoApplication, ProtoDataCollectionInstance
from proto.form_runner.helpers import get_answer_text_for_question_from_section_data


def serialize_collection_data(collection: ProtoDataCollectionInstance) -> dict[str, dict[str, Any]]:
    data = defaultdict(dict)

    for section in collection.section_data:
        for question in section.section.questions:
            data[section.section.slug.replace("-", "_")][question.slug.replace("-", "_")] = (
                get_answer_text_for_question_from_section_data(question, section)
            )

    return data


def build_context_injector(
    this_collection: ProtoDataCollectionInstance, application: ProtoApplication | None = None
) -> Callable[[str], str]:
    # It would be nice if "this collection"s data was somehow surfaced at the top-level, ie not namespaced, but
    # would need to give due consideration to namespace collisions. So I'm skipping that for now by having everything
    # namespaced.
    # I think it might be "nice" / "more usable" if the following stuff was available at the top-level:
    # - References to the questions in the "current" section
    # - References to sections in the "current" collection
    # - Then references to related objects, eg if we're doing monitoring, then the application, grant recipient, etc
    context = {
        "this_collection": serialize_collection_data(this_collection),
    }

    if application:
        context["application"] = serialize_collection_data(application.data_collection_instance)

    return functools.partial(interpolate, context=context)


def interpolate(text: str, context: dict) -> str:
    evaluator = simpleeval.EvalWithCompoundTypes(names=context)

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
        }
    }

    return re.sub(r"\(\((.*?)\)\)", lambda m: evaluator.eval(m.group(1)), text)
