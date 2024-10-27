from fastapi import FastAPI

# Импортируем главный роутер.
from app.api.routers import main_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.app_title,
              description="API_DESC",
              version="0.2.0",
              docs_url='/docs',
              redoc_url='/redoc',
              openapi_url='/openapi.json'
              )
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники или укажите нужные
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)

# Подключаем главный роутер.
app.include_router(main_router)