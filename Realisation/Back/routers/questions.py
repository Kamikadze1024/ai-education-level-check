from fastapi import APIRouter
from schemas.questions import QuestionsRequest, QuestionsResponse
from services.questions import generate_questions


router = APIRouter()

@router.post("/questions", response_model=QuestionsResponse)
def get_questions(request: QuestionsRequest):
    """
    Генерирует вопросы на основе предоставленных данных.
    """
    questions = generate_questions(
        num_questions=request.num_questions,
        num_answ_per_one_quest=request.num_answ_per_one_quest,
        num_correct_answ_per_one_quest=request.num_correct_answ_per_one_quest  # сейчас стоит заглушка в функции->вернет none
    )
    return questions
