from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, default="другое")
    estimated_minutes = Column(Integer, default=30)
    complexity = Column(String, default="medium")
    completed = Column(Boolean, default=False)
