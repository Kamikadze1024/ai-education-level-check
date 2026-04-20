# Временная "база данных" — просто список в памяти

QUESTIONS_STORAGE = []

def save_questions(data: dict) -> int:
    """
    Сохраняем список вопросов и ответов в хранилище.
    Возвращаем идентификатор сохранённого списка.
    """
    QUESTIONS_STORAGE.append(data)
    quest_list_id = len(QUESTIONS_STORAGE)  # id = порядковый номер в списке
    return quest_list_id