from fastapi import FastAPI
from routers import auth, upload, questions
import uvicorn


# Создаем FastAPI приложение
app = FastAPI(
    title="AI Ed Tech Exam API"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 

# Подключаем роутеры для разных функциональностей
app.include_router(auth.router, prefix="/core", tags=["auth"])
# app.include_router(upload.router, prefix="/core", tags=["upload"])
# app.include_router(questions.router, prefix="/core", tags=["questions"])



# точка входа в программу
if __name__ == "__main__":
    print("Backend")

    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000,
        log_level="info",
        reload=True 
    )
