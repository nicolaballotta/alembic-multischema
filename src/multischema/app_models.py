from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .db.base import AppBase
from .core_models import User


class Business(AppBase):
    __tablename__ = 'business'
    __table__args__ = {'schema': 'app'}
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    user = relationship('User', backref='businesses', cascade="all, delete-orphan")
