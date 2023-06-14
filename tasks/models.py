from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, UniqueConstraint

from datetime import datetime

from database import Base
from auth.models import User


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=128), nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey(User.id))

    __table_args__ = (
        UniqueConstraint(title, description, user_id, name='task_unique_title_description_user_id'),
    )
