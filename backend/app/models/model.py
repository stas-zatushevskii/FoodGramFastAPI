from sqlalchemy import Column, String

from backend.app.core.db import Base


class TestBase(Base):
    name = Column(String(100), unique=True, nullable=False)