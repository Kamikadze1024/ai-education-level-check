from pydantic import BaseModel

# --- Запрос ---
class QuestionsRequest(BaseModel):
    num_questions: int # кол-во вопросов
    num_answ_per_one_quest: int # кол-во вариантов ответа на один вопрос    
    num_correct_answ_per_one_quest: int # кол-во правильных ответов на один вопрос

# --- Ответ ---
class Answer(BaseModel):
    answ_txt: str

class Question(BaseModel):
    question_num: int
    question_txt: str
    correct_answs: list[Answer]
    not_correct_answs: list[Answer]

class QuestionsResponse(BaseModel):
    msg_type: str # просто название поля (постоянно)
    questions: list[Question]