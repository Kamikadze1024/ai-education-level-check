import os
import shutil
from fastapi import UploadFile

# Папка для сохранения файлов
UPLOAD_DIR = "uploads"

# Разрешённые расширения файлов
EXTENSIONS = {".pdf", ".docx", ".txt", ".doc", ".md"}

def validate_file(filename: str) -> bool:
    """Проверяем, что расширение файла разрешено"""

    _, ext = os.path.splitext(filename)
    return ext.lower() in EXTENSIONS

def save_file(file: UploadFile) -> str:
    """Сохраняем файл на диск и возвращаем путь к нему"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Открываем файл на диск и копируем в него содержимое загрузки

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)       

    return file_path    




    