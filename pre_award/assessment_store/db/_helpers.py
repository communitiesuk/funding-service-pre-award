import jsonpath_rw_ext


def get_answer_value(application_json, answer_key):
    question = jsonpath_rw_ext.parse(f"$.forms[*].questions[*].fields[?(@.key == '{answer_key}')]").find(
        application_json
    )
    if question:
        return question[0].value["answer"]
    else:
        return "Not Available"
