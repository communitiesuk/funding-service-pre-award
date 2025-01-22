from typing import NewType, TypedDict

pk_int = NewType("pk_int", int)
dict_or_list_or_none = list | None
QuestionChoice = TypedDict("QuestionChoice", value=str, label=str)
t_data_source = NewType("t_data_source", list[QuestionChoice, ...] | None)
