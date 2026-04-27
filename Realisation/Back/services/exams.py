from services.save_questions import QUESTIONS_STORAGE

def get_available_exams() -> list[int]:
    """
    Возвращаем список id всех доступных экзаменов.
    Берём из того же хранилища куда сохраняли вопросы.
    """
    return list(range(1, len(QUESTIONS_STORAGE) + 1))  
def get_exam_by_id(exam_id: int) -> dict | None:
   
    """
    Возвращаем данные экзамена по ID.
    
    """
    if exam_id < 1 or exam_id > len(QUESTIONS_STORAGE):
        return None  # экзамен с таким ID не найден
  

    return QUESTIONS_STORAGE[exam_id - 1]  # достаём из базы данных
