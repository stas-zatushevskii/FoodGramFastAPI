from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        # Именем таблицы будет название модели в нижнем регистре.
        return cls.__name__.lower()

    # Во все таблицы будет добавлено поле ID.
    id = Column(Integer, primary_key=True)


# базовый класс для будущих моделей:
# В качестве основы для базового класса укажем класс PreBase.
Base = declarative_base(cls=PreBase)


# создания асинхронного движка
engine = create_async_engine(settings.database_url)

# создание множественных сесий с помощью sessionmaker
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)