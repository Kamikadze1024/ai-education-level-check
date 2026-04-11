from fastapi import APIRouter, UploadFile, File
from schemas.upload import UploadResponse
from services.upload import validate_file, save_file

router = APIRouter()

@router.post("/upload_know_base", response_model=UploadResponse)
def upload_knowledge_base(file: UploadFile = File(...)):
    """
POST /gen/upload_know_base
Принимаем файл, проверяем, сохраняем на диск
"""
# проверяем расширение
    if not validate_file(file.filename):
        return UploadResponse(
            result="fail",
            filename=file.filename,
            message="Недопустимый тип файла. Разрешены: pdf, txt, doc, docx, md"
        )

 # сохраняем файл
    try:
        file_path = save_file(file)
        return UploadResponse(
            result="ok",
            filename=file.filename,
            message=f"Файл успешно сохранён: {file_path}"
        )
    except Exception as e:
        return UploadResponse(
            result="fail",
            filename=file.filename,
            message=f"Ошибка при сохранении файла: {str(e)}"
        )
    
    