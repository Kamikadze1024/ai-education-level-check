"""
Файл с настройками проекта. 
Реализована загрузка API ключа из файла .env для последующих импортов
"""


import os
from dotenv import load_dotenv

load_dotenv()

GIGA_API_KEY = os.getenv("GIGA_API_KEY")

