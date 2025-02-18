from proto.common.data.models import (
    ProtoDataCollectionDefinitionQuestion,
    ProtoDataCollectionDefinitionSection,
)
from proto.common.data.models.data_collection import (
    ConditionCombination,
    ProtoDataCollectionInstanceSectionData,
    ProtoDataCollectionQuestionCondition,
)
from proto.form_runner.helpers import (
    get_answer_value_for_question_from_section_data,
)


def get_visible_questions_for_section_instance(
    section_definition: ProtoDataCollectionDefinitionSection,
    section_instance_data: ProtoDataCollectionInstanceSectionData,
):
    visible_questions = []
    for question in section_definition.questions:
        if not question.conditions:
            visible_questions.append(question)
            continue

        condition_combo_operator = question.condition_combination_type

        condition_results = []
        for condition in question.conditions:
            condition_results.append(evaluate_condition(condition=condition, section_data=section_instance_data))

        if condition_combo_operator == ConditionCombination.AND:
            if all(condition_results):
                visible_questions.append(question)

        if condition_combo_operator == ConditionCombination.OR:
            if any(condition_results):
                visible_questions.append(question)
    return visible_questions


def evaluate_condition(
    section_data: ProtoDataCollectionInstanceSectionData, condition: ProtoDataCollectionQuestionCondition
) -> bool:
    depends_on_answer_text = get_answer_value_for_question_from_section_data(
        section_data=section_data, question=condition.depends_on_question
    )

    operator = condition.criteria["operator"]
    value_to_compare = condition.criteria["value"]

    match operator:
        case "EQUALS":
            return value_to_compare == depends_on_answer_text
        case "GREATER":
            return value_to_compare > depends_on_answer_text
        case "LESS":
            return value_to_compare < depends_on_answer_text
        case _:
            return False


def get_next_question_for_data_collection_instance(
    section_instance_data: ProtoDataCollectionInstanceSectionData,
    current_question_definition: ProtoDataCollectionDefinitionQuestion,
) -> ProtoDataCollectionDefinitionQuestion | None:
    visible_questions = get_visible_questions_for_section_instance(
        current_question_definition.section, section_instance_data
    )

    index_current_question = visible_questions.index(current_question_definition)
    if index_current_question == len(visible_questions) - 1:
        return None
    return visible_questions[index_current_question + 1]
