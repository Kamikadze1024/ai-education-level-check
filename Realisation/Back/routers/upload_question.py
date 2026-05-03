from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas.upload import UploadResponse
from services.upload import validate_file, save_file, load_knowledge_base
from schemas.questions import QuestionsRequest, QuestionsResponse
from services.questions import generate_questions
from schemas.save_questions import SaveQuestionsRequest, SaveQuestionsResponse
from services.save_questions import save_questions




router = APIRouter(prefix="/gen")


@router.post("/upload_know_base", response_model=UploadResponse)
def upload_knowledge_base(file: UploadFile = File(...)):
    """
    POST /gen/upload_know_base
    Принимаем файл, проверяем, сохраняем на диск
    """      
    try:
        # проверяем расширение файла
        if not validate_file(file.filename):
            raise HTTPException(
                status_code=400,  # Bad Request — клиент прислал недопустимый файл
                detail="Недопустимый тип файла. Разрешены: pdf, txt, doc, docx, md"
            )

        # сохраняем файл на диск
        file_path = save_file(file)

        # звгружаем базу знаний из папки uploads через функцию из loader.py, сохраняем чанки в глобальную переменную
        load_knowledge_base()

        # успех — HTTP 200
        return UploadResponse(
            result="ок",
            filename=file.filename,
            message=f"Файл сохранён: {file_path}. База знаний загружена."
        )

    except HTTPException:
        raise  # пробрасываем наш HTTPException дальше, не перехватываем

    except Exception:
        # непредвиденная ошибка сервера — HTTP 500
        raise HTTPException(
            status_code=500,
            detail="Что-то пошло не так при загрузке файла..."
        )


    

@router.post("/questions", response_model=QuestionsResponse)
def get_questions(request: QuestionsRequest):
    """
    Генерирует вопросы и ответы на основе предоставленных данных.
    """
    try:
        # валидация: правильных не может быть больше или равно общему кол-ву ответов
        if request.num_correct_answ_per_one_quest >= request.num_answ_per_one_quest:
            raise HTTPException(
                status_code=400,
                detail="Кол-во правильных ответов должно быть меньше общего кол-ва ответов"
            )

        # генерируем вопросы из мок-набора
        return generate_questions(
            num_questions=request.num_questions,
            num_answ_per_one_quest=request.num_answ_per_one_quest,
            num_correct_answ_per_one_quest=request.num_correct_answ_per_one_quest
        )

    except HTTPException:
        raise  # пробрасываем дальше, не перехватываем

    except Exception:
      
        raise HTTPException(
            status_code=500,
            detail="Что-то пошло не так при генерации вопросов..."
        )
    
    
@router.post("/save_questions", response_model=SaveQuestionsResponse)
def save_questions_route(request: SaveQuestionsRequest):
    try:
        # сохраняем список вопросов в хранилище
        quest_list_id = save_questions(request.model_dump())

        # успех — возвращаем id сохранённого списка, HTTP 200
        return SaveQuestionsResponse(quest_list_id=quest_list_id)

    except HTTPException:
        raise  # пробрасываем дальше, не перехватываем

    except Exception:
        # непредвиденная ошибка — HTTP 500
        raise HTTPException(
            status_code=500,
            detail="Что-то пошло не так при сохранении вопросов..."
        )    
    