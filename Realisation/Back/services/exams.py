from services.save_questions import QUESTIONS_STORAGE

def get_available_exams() -> list[int]:
    """
    Возвращаем список id всех доступных экзаменов.
    Берём из того же хранилища куда сохраняли вопросы.
    """
    return list(range(1, len(QUESTIONS_STORAGE) + 1))  