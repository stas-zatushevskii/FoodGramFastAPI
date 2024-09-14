from sqlalchemy import Column, String

from app.core.db import Base


class TestBase(Base):
    name = Column(String(100), unique=True, nullable=False)