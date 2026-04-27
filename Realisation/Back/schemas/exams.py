from pydantic import BaseModel
from schemas.questions import Question

class AvailableExam(BaseModel):
    available_exam_id: int       # идентификатор доступного списка вопросов

class AvailableExamsResponse(BaseModel):
    available_exams: list[AvailableExam]  # список доступных экзаменов

class GetExamByIdRequest(BaseModel):
    exam_id: int       # идентификатор экзамена, выбранный студентом

class GetExamByIdResponse(BaseModel):
    msg_type: str                   # тип сообщения 
    questions: list[Question]       # список вопросов, входящих в экзамен



