from pydantic import BaseModel

class AvailableExam(BaseModel):
    available_exam_id: int       # идентификатор доступного списка вопросов

class AvailableExamsResponse(BaseModel):
    available_exams: list[AvailableExam]  # список доступных экзаменов