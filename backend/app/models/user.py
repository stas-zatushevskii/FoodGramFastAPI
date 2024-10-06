from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base # noqa

from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship, WriteOnlyMapped

from sqlalchemy.orm import relationship, Mapped, mapped_column

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
    # Установите связь между моделями через функцию relationship.
    # User OneToMany -> Recipe
    recipe = relationship('Recipe', cascade='delete')
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