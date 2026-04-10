"""
Файл с настройками проекта. 
Реализована загрузка API ключа из файла .env для последующих импортов
"""


import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

