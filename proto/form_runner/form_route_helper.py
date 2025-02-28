from proto.common.data.models import (
    ProtoDataCollectionDefinitionQuestion,
    ProtoDataCollectionDefinitionSection,
)
from proto.common.data.models.data_collection import (
    ConditionCombination,
    ProtoDataCollectionInstanceSectionData,
    ProtoDataCollectionQuestionCondition,
)
from proto.form_runner.expressions import build_context_evaluator


def get_visible_questions_for_section_instance(
    section_definition: ProtoDataCollectionDefinitionSection,
    section_instance_data: ProtoDataCollectionInstanceSectionData,
) -> list[ProtoDataCollectionDefinitionQuestion]:
    visible_questions = []
    for question in section_definition.questions:
        if not question.conditions:
            visible_questions.append(question)
            continue

        condition_combo_operator = question.condition_combination_type

        condition_results = []
        for condition in question.conditions:
            condition_results.append(
                evaluate_condition(condition=condition, all_section_data=section_instance_data.instance.section_data)
            )

        if condition_combo_operator == ConditionCombination.AND:
            if all(condition_results):
                visible_questions.append(question)

        if condition_combo_operator == ConditionCombination.OR:
            if any(condition_results):
                visible_questions.append(question)
    return visible_questions


def evaluate_condition(
    all_section_data: list[ProtoDataCollectionInstanceSectionData], condition: ProtoDataCollectionQuestionCondition
) -> bool:
    context_evaluator = build_context_evaluator(this_collection=all_section_data[0].instance, answer=None)
    return bool(context_evaluator(condition.expression))


def get_next_question_for_data_collection_instance(
    section_instance_data: ProtoDataCollectionInstanceSectionData,
    current_question_definition: ProtoDataCollectionDefinitionQuestion,
):
    visible_questions = get_visible_questions_for_section_instance(
        current_question_definition.section, section_instance_data
    )

    index_current_question = visible_questions.index(current_question_definition)
    if index_current_question == len(visible_questions) - 1:
        return None
    return visible_questions[index_current_question + 1]


# assumes you're not going to land here from the 0th (given logic elsewhere)
# we'd want to check that anyay for real (these should also just be helpers on a nice class)
def get_previous_question_for_data_collection_instance(
    section_instance_data: ProtoDataCollectionInstanceSectionData,
    current_question_definition: ProtoDataCollectionDefinitionQuestion,
):
    visible_questions = get_visible_questions_for_section_instance(
        current_question_definition.section, section_instance_data
    )

    index_current_question = visible_questions.index(current_question_definition)
    return visible_questions[index_current_question - 1]
