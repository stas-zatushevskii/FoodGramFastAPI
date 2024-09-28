from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base # noqa

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship


class User(SQLAlchemyBaseUserTable[int], Base):
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
    subscription = relationship('Subscription', cascade='delete')
