import base64
import os
from typing import Optional
from uuid import uuid4

from sqlalchemy import select

from app.core.db import AsyncSession
from app.models import User

"""
При работе с асинхронным движком (engine) SQLAlchemy запросы к БД можно писать только в стиле 2.0.
В SQLAlchemy стилем 1.x называются запросы, которые поддерживаются в версиях 1.3 и ранее. В январе
2023 вышла SQLAlchemy версии 2.0; в этой версии синтаксис запросов немного иной, чем в 1.x. Именно
этот синтаксис и называется «стиль 2.0». Версия библиотеки 1.4 поддерживает оба стиля запросов
(1.x и 2.0) в случае обычного (синхронного) исполнения, и только стиль 2.0 для асинхронных 
запросов."""


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["author_id"] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def save_image(
        self,
        image,
    ):
        # Генерация уникального имени файла для изображения
        filename = f"{uuid4()}.png"
        file_location = os.path.join("media/recipes/images/", filename)
        # Удаление префикса 'data:image/png;base64,' если он есть
        header, base64_str = image.split(",", 1) if "," in image else (None, image)
        # Декодирование строки Base64
        image_data = base64.b64decode(base64_str)
        # Сохранение картинки
        with open(file_location, "wb") as file:
            file.write(image_data)
        filename_url = f"/media/recipes/images/{filename}"
        return filename_url

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def delete(
        self,
        db_obj,
        session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj
