from pydantic import BaseModel


# --- Запрос ---
class UserAnswer(BaseModel):
    answ_txt: str  # текст ответа пользователя


class QuestionAnswer(BaseModel):
    question_num: int  # номер вопроса
    user_answs: list[UserAnswer]  # ответы пользователя на этот вопрос


class ExamExecuteRequest(BaseModel):
    msg_type: str  # "exam_procedure" (постоянно)
    answers: list[QuestionAnswer]  # список ответов на все вопросы


# --- Ответ ---
class ExamExecuteResponse(BaseModel):
    correct_answs: int  # количество правильных ответов
    incorrect_answs: int  # количество неправильных ответов
