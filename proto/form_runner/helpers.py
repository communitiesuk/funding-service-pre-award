from proto.common.data.models import ProtoDataCollectionQuestion, ProtoDataCollectionSectionData
from proto.common.data.models.question_bank import QuestionType


def get_answer_text_for_question_from_section_data(
    question: ProtoDataCollectionQuestion, section_data: ProtoDataCollectionSectionData
):
    answer_id = str(question.id)
    return get_answer_text_for_question(question, section_data.data.get(answer_id, {}).get("answer"))


def get_answer_text_for_question(question: ProtoDataCollectionQuestion, answer_data):
    if not answer_data:
        return None

    if question.type == QuestionType.RADIOS:
        return answer_data["label"]

    return answer_data


def get_answer_value_for_question(question: ProtoDataCollectionQuestion, answer_data):
    if not answer_data:
        return None

    if question.type == QuestionType.RADIOS:
        return answer_data["value"]

    return answer_data
