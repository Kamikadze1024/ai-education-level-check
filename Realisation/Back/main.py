from fastapi import FastAPI
from routers import upload_question, auth, exams
from middleware.logging import log_requests
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

# Создаем FastAPI приложение
app = FastAPI(title="AI Ed Tech Exam API")

# добавляем middleware для логирования запросов
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Подключаем роутеры для разных функциональностей
app.include_router(auth.router)
app.include_router(upload_question.router)
app.include_router(exams.router)


# точка входа в программу
if __name__ == "__main__":
    print("Backend")

    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000, log_level="info", reload=True
    )
