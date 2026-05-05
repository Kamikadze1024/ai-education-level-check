from pydantic import BaseModel


# --- Запрос ---
class QuestionsRequest(BaseModel):
    num_questions: int  # кол-во вопросов
    num_answ_per_one_quest: int  # кол-во вариантов ответа на один вопрос
    num_correct_answ_per_one_quest: (
        int  # кол-во правильных ответов на один вопрос
    )


# --- Ответ ---
class Answer(BaseModel):
    answ_txt: str  # текст ответа


class Question(BaseModel):
    question_num: int  # номер вопроса
    question_txt: str  # текст вопроса
    correct_answs: list[Answer]  # правильные ответы
    not_correct_answs: list[Answer]  # неправильные ответы


class QuestionsResponse(BaseModel):
    msg_type: str  # просто название поля (постоянно)
    questions: list[Question]  # список вопросов с ответами
