from services.save_questions import QUESTIONS_STORAGE


def check_answers(answers: list[dict]) -> dict:
    """
    Проверяем ответы пользователя по сохранённым вопросам.
    Возвращаем количество правильных и неправильных ответов.
    """
    correct = 0
    incorrect = 0

    for user_answer in answers:
        question_num = user_answer["question_num"]  # номер вопроса

        # ищем вопрос в хранилище по номеру
        question = None
        for saved in QUESTIONS_STORAGE:
            for q in saved["questions"]:
                if q["question_num"] == question_num:
                    question = q
                    break

        if question is None:
            # вопрос не найден в хранилище — считаем неправильным
            incorrect += 1
            continue

        # собираем тексты правильных ответов из хранилища
        correct_texts = {a["answ_txt"] for a in question["correct_answs"]}

        # собираем тексты ответов пользователя
        user_texts = {a["answ_txt"] for a in user_answer["user_answs"]}

        # сравниваем — если совпадают полностью, ответ правильный
        if user_texts == correct_texts:
            correct += 1
        else:
            incorrect += 1

    return {"correct_answs": correct, "incorrect_answs": incorrect}
