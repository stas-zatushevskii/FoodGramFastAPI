from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from .config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()


Base = declarative_base(cls=PreBase)


# создания асинхронного движка
engine = create_async_engine(settings.database_url)

# создание множественных сесий с помощью sessionmaker
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Асинхронный генератор сессий.
async def get_async_session():
    # Через асинхронный контекстный менеджер и sessionmaker
    # открывается сессия.
    async with AsyncSessionLocal() as async_session:
        # Генератор с сессией передается в вызывающую функцию.
        yield async_session
        # Когда HTTP-запрос отработает - выполнение кода вернётся сюда,
        # и при выходе из контекстного менеджера сессия будет закрыта.
