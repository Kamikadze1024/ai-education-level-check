"""
Файл с настройками проекта.
Реализована загрузка API ключа из файла из yml с fallback .env для последующих импортов
"""

import os
import yaml
from dotenv import load_dotenv

load_dotenv()

GIGA_API_KEY = os.getenv("GIGA_API_KEY")

# читаем какую LLM использовать
with open("settings.yaml", "r", encoding="utf-8") as f:
    LLM_PROVIDER = yaml.safe_load(f).get("llm_provider", "local")



# # пробуем прочитать ключ из api_keys.yml
# def _load_from_yaml() -> str | None:
#     try:
#         with open("api_keys.yml", "r", encoding="utf-8") as f:
#             data = yaml.safe_load(f)
#             return data.get("gigachat_api_key")
#     except FileNotFoundError:
#         return None


# # сначала берём из yml, если нет — из .env
# GIGA_API_KEY = _load_from_yaml() or os.getenv("GIGA_API_KEY")
