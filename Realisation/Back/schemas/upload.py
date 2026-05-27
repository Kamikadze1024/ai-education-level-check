from pydantic import BaseModel


class UploadResponse(BaseModel):
    result: str  # результат загрузки ("ok" или "fail")
    filename: str  # имя сохраненного файла
    message: str  # сообщение
