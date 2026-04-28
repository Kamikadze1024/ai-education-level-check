from fastapi import APIRouter, HTTPException
from schemas.exams import AvailableExamsResponse, AvailableExam, GetExamByIdRequest, GetExamByIdResponse
from schemas.questions import Question, Answer
from services.exams import get_available_exams, get_exam_by_id
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

@router.post("/get_exam_by_id", response_model=GetExamByIdResponse)
def get_exam_by_id_route(request: GetExamByIdRequest):
    """
    POST /exam/get_exam_by_id
    Возвращаем вопросы конкретного экзамена по его ID
    """
    try:
        exam_data = get_exam_by_id(request.exam_id)

        if exam_data is None:
            raise HTTPException(
                status_code=404,  # Not Found — экзамен с таким ID не найден
                detail=f"Экзамен с ID={request.exam_id} не найден"
            )

        # восстанавливаем Pydantic-объекты из словаря
        questions = [
            Question(
                question_num=q["question_num"],
                question_txt=q["question_txt"],
                correct_answs=[Answer(answ_txt=a["answ_txt"]) for a in q["correct_answs"]],
                not_correct_answs=[Answer(answ_txt=a["answ_txt"]) for a in q["not_correct_answs"]]
            )
            for q in exam_data["questions"]
        ]

        # успех — возвращаем структуру идентичную сохранённой в базу, HTTP 200
        return GetExamByIdResponse(
            msg_type=exam_data.get("msg_type", "questions_list"),
            questions=questions
        )

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Что-то пошло не так при получении экзамена...")


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
    