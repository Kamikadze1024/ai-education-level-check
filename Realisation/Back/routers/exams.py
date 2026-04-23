from fastapi import APIRouter, HTTPException
from schemas.exams import AvailableExamsResponse, AvailableExam
from services.exams import get_available_exams
from schemas.exam_execute import ExamExecuteRequest, ExamExecuteResponse
from services.exam_execute import check_answers


router = APIRouter(prefix="/exam")

@router.get("/get_available_exams", response_model=AvailableExamsResponse)
def available_exams():
    try:
        # получаем список id доступных экзаменов
        exam_ids = get_available_exams()

        # формируем список объектов AvailableExam
        exams = [AvailableExam(available_exam_id=exam_id) for exam_id in exam_ids]

        # успех — HTTP 200
        return AvailableExamsResponse(available_exams=exams)

    except HTTPException:
        raise  # пробрасываем дальше, не перехватываем

    except Exception:
        # непредвиденная ошибка — HTTP 500
        raise HTTPException(
            status_code=500,
            detail="Что-то пошло не так при получении списка экзаменов..."
        )
    
@router.post("/execute", response_model=ExamExecuteResponse)
def execute_exam(request: ExamExecuteRequest):
    try:
        # проверяем ответы пользователя
        result = check_answers(request.model_dump()["answers"])

        # успех — HTTP 200
        return ExamExecuteResponse(
            correct_answs=result["correct_answs"],
            incorrect_answs=result["incorrect_answs"]
        )

    except HTTPException:
        raise  # пробрасываем дальше, не перехватываем

    except Exception:
        # непредвиденная ошибка — HTTP 500
        raise HTTPException(
            status_code=500,
            detail="Что-то пошло не так при проведении тестирования..."
        )
    