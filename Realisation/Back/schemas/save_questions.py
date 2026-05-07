from pydantic import BaseModel
from schemas.questions import Question


class SaveQuestionsRequest(BaseModel):
    msg_type: str  # "questions_list"
    questions: list[Question]  # список вопросов и ответов из /gen/questions


class SaveQuestionsResponse(BaseModel):
    quest_list_id: int  # идентификатор сохранённого списка вопросов
