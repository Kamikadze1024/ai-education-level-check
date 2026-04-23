from schemas.questions import QuestionsResponse

def generate_questions(
    num_questions: int,  # к-во запросов
    num_answ_per_one_quest: int,  # к-во вариантов ответа на один вопрос
    num_correct_answ_per_one_quest: int  # к-во правильных ответов на один вопрос
) -> QuestionsResponse:
    #  TODO реализовать генерацию вопросов и ответов
    pass

# вывод JSON:
# {{
#         "msg_type": "questions_list",
#         "questions": [
#             {{
#                 "question_num": 1,
#                 "question_txt": "текст вопроса",
#                 "correct_answs": [
#                     {{"answ_txt": "текст правильного ответа"}}
#                 ],
#                 "not_correct_answs": [
#                     {{"answ_txt": "текст неправильного ответа"}}
#                 ]
#             }}
#         ]
#     }}

#   Парсим JSON который вернет LLM
#   data = json.loads(raw_text)

#  Превращаем словарь в Pydantic-модель (для проверки структуры)
#  return QuestionsResponse(**data)
#  
