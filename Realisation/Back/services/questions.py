import random
import json
from schemas.questions import QuestionsResponse, Question, Answer
from LLM.loader import gen_questions          
import services.upload as upload_service   

# Захардкоженные наборы вопросов 
# MOCK_QUESTIONS_SETS = [
#     # Набор 1 
#     {
#         "msg_type": "questions_list",
#         "questions": [
#             {
#                 "question_num": 1,
#                 "question_txt": "Что такое ВВП?",
#                 "correct_answs": [
#                     {"answ_txt": "Рыночная стоимость всех товаров и услуг произведённых в стране за год"}
#                 ],
#                 "not_correct_answs": [
#                     {"answ_txt": "Сумма всех налогов собранных государством за год"},
#                     {"answ_txt": "Общий объём экспорта страны за год"},
#                     {"answ_txt": "Сумма всех банковских вкладов населения"}
#                 ]
#             },
#             {
#                 "question_num": 2,
#                 "question_txt": "Что такое инфляция?",
#                 "correct_answs": [
#                     {"answ_txt": "Устойчивый рост общего уровня цен на товары и услуги"}
#                 ],
#                 "not_correct_answs": [
#                     {"answ_txt": "Снижение курса национальной валюты"},
#                     {"answ_txt": "Рост государственного долга"},
#                     {"answ_txt": "Уменьшение объёма денежной массы в экономике"}
#                 ]
#             },
#             {
#                 "question_num": 3,
#                 "question_txt": "Что такое рецессия?",
#                 "correct_answs": [
#                     {"answ_txt": "Спад экономической активности продолжающийся два квартала подряд"}
#                 ],
#                 "not_correct_answs": [
#                     {"answ_txt": "Рост уровня безработицы выше 10%"},
#                     {"answ_txt": "Снижение курса акций на фондовом рынке"},
#                     {"answ_txt": "Дефицит государственного бюджета"}
#                 ]
#             }
#         ]
#     },
#     # Набор 2 
#     {
#         "msg_type": "questions_list",
#         "questions": [
#             {
#                 "question_num": 1,
#                 "question_txt": "Что такое эластичность спроса?",
#                 "correct_answs": [
#                     {"answ_txt": "Чувствительность величины спроса к изменению цены товара"}
#                 ],
#                 "not_correct_answs": [
#                     {"answ_txt": "Способность рынка быстро реагировать на новые товары"},
#                     {"answ_txt": "Гибкость ценообразования в условиях монополии"},
#                     {"answ_txt": "Изменение предложения товара при росте производства"}
#                 ]
#             },
#             {
#                 "question_num": 2,
#                 "question_txt": "Что такое монополия?",
#                 "correct_answs": [
#                     {"answ_txt": "Рыночная структура где один продавец контролирует весь рынок"}
#                 ],
#                 "not_correct_answs": [
#                     {"answ_txt": "Рынок где несколько крупных компаний делят сферы влияния"},
#                     {"answ_txt": "Государственное регулирование цен на товары"},
#                     {"answ_txt": "Соглашение между компаниями о фиксации цен"}
#                 ]
#             },
#             {
#                 "question_num": 3,
#                 "question_txt": "Что такое предельные издержки?",
#                 "correct_answs": [
#                     {"answ_txt": "Затраты на производство одной дополнительной единицы товара"}
#                 ],
#                 "not_correct_answs": [
#                     {"answ_txt": "Минимальные затраты необходимые для запуска производства"},
#                     {"answ_txt": "Общие затраты разделённые на объём производства"},
#                     {"answ_txt": "Постоянные затраты не зависящие от объёма выпуска"}
#                 ]
#             }
#         ]
#     },
#     # Набор 3 
#     {
#         "msg_type": "questions_list",
#         "questions": [
#             {
#                 "question_num": 1,
#                 "question_txt": "Что такое ключевая ставка центрального банка?",
#                 "correct_answs": [
#                     {"answ_txt": "Процентная ставка по которой ЦБ выдаёт кредиты коммерческим банкам"}
#                 ],
#                 "not_correct_answs": [
#                     {"answ_txt": "Минимальная ставка по вкладам для физических лиц"},
#                     {"answ_txt": "Ставка налога на прибыль банков"},
#                     {"answ_txt": "Максимальная ставка по потребительским кредитам"}
#                 ]
#             },
#             {
#                 "question_num": 2,
#                 "question_txt": "Что такое диверсификация портфеля?",
#                 "correct_answs": [
#                     {"answ_txt": "Распределение инвестиций между разными активами для снижения риска"}
#                 ],
#                 "not_correct_answs": [
#                     {"answ_txt": "Вложение всех средств в наиболее доходный актив"},
#                     {"answ_txt": "Стратегия покупки акций только одной отрасли"},
#                     {"answ_txt": "Перевод активов в иностранную валюту"}
#                 ]
#             },
#             {
#                 "question_num": 3,
#                 "question_txt": "Что такое ликвидность актива?",
#                 "correct_answs": [
#                     {"answ_txt": "Способность актива быстро превращаться в деньги без потери стоимости"}
#                 ],
#                 "not_correct_answs": [
#                     {"answ_txt": "Доходность актива за определённый период"},
#                     {"answ_txt": "Рыночная стоимость актива на текущий момент"},
#                     {"answ_txt": "Степень риска вложений в данный актив"}
#                 ]
#             }
#         ]
#     }
# ]


# def generate_questions(
#     num_questions: int,  # к-во запросов
#     num_answ_per_one_quest: int,  # к-во вариантов ответа на один вопрос
#     num_correct_answ_per_one_quest: int  # к-во правильных ответов на один вопрос
# ) -> QuestionsResponse:
#     # выбираем случайный набор вопросов из захардкоженных
#     mock_set = random.choice(MOCK_QUESTIONS_SETS)

#     # берём только нужное количество вопросов
#     selected_questions = mock_set["questions"][:num_questions]

#     questions = []
#     for q in selected_questions:
#         # берём только нужное количество правильных ответов
#         correct = q["correct_answs"][:num_correct_answ_per_one_quest]

#         # вычисляем сколько неправильных нужно
#         num_incorrect = num_answ_per_one_quest - num_correct_answ_per_one_quest
#         incorrect = q["not_correct_answs"][:num_incorrect]

#         questions.append(Question(
#             question_num=q["question_num"],
#             question_txt=q["question_txt"],
#             correct_answs=[Answer(answ_txt=a["answ_txt"]) for a in correct],
#             not_correct_answs=[Answer(answ_txt=a["answ_txt"]) for a in incorrect]
#         ))

#     return QuestionsResponse(
#         msg_type="questions_list",
#         questions=questions
#     )
    
def generate_questions(
    num_questions: int,
    num_answ_per_one_quest: int,
    num_correct_answ_per_one_quest: int
) -> QuestionsResponse:
    """Генерируем вопросы через GigaChat на основе загруженных чанков."""

    chunks = upload_service.loaded_chunks

   
    # вызываем gen_questions из LLM/loader.py
    raw_json = gen_questions(
        chunks=chunks,
        n=num_questions,
        m=num_answ_per_one_quest,
        k=num_correct_answ_per_one_quest
    )

    # парсим JSON и превращаем в Pydantic-схему
    data = json.loads(raw_json)
    return QuestionsResponse(**data)
   
