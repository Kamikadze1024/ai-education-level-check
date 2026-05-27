import logging
import time
from fastapi import Request

# настраиваем логгер — пишем в файл и в консоль одновременно
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",  # метка времени | сообщение
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),  # пишем в файл
        logging.StreamHandler(),  # пишем в консоль
    ],
)
logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    """
    Middleware — перехватывает каждый запрос.
    Логгирует: метод, url, входные параметры, время ответа, статус код.
    """
    # --- до выполнения запроса ---
    start_time = time.time()

    # читаем тело запроса (входные параметры)
    body = await request.body()
    # body_str = body.decode("utf-8") if body else "нет тела"

    try:
        body_str = body.decode("utf-8")
    except UnicodeDecodeError:
        body_str = f"<бинарные данные, {len(body)} байт>"

    # --- выполняем запрос ---
    response = await call_next(request)

    # --- после выполнения запроса ---
    duration = round(time.time() - start_time, 3)  # время выполнения в секундах

    logger.info(
        f"\n"
        f"  метод:      {request.method} {request.url}\n"
        f"  параметры:  {body_str}\n"
        f"  статус:     {response.status_code}\n"
        f"  время:      {duration} сек"
    )

    return response
