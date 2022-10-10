from sqlalchemy import Column, Integer, String
from .db.base import Base


class User(Base):
    __tablename__ = "user"
    __table__args__ = {'schema': 'core'}
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)