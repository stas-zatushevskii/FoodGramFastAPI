from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Table, Text)
from sqlalchemy.orm import Mapped, WriteOnlyMapped, mapped_column, relationship

from app.core.db import Base  # noqa

followers = Table(
    'followers',
    Base.metadata,
    Column('author_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('follower_id', Integer, ForeignKey('user.id'), primary_key=True)
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id = mapped_column(Integer, primary_key=True)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    username: str = Column(String, nullable=False)
    # Установите связь между моделями через функцию relationship.
    # User OneToMany -> Recipe
    recipes = relationship("Recipe", back_populates="author")
    # Установите связь между моделями через функцию relationship.
    # User ManyToMany -> Subscription
    # Пользователи, на которых подписан текущий пользователь

    followings: Mapped[List['User']] = relationship(
        'User',
        secondary=followers,
        primaryjoin=id == followers.c.follower_id,
        secondaryjoin=id == followers.c.author_id,
        back_populates='followers',
    )

    followers: Mapped[List['User']] = relationship(
        'User',
        secondary=followers,
        primaryjoin=id == followers.c.author_id,
        secondaryjoin=id == followers.c.follower_id,
        back_populates='followings',
    )