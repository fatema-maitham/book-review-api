from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel

class BookModel(BaseModel):
  __tablename__ = "books"

  title = Column(String, nullable=False)
  author = Column(String, nullable=False)
  description = Column(String, nullable=True)

  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

  user = relationship("UserModel", back_populates="books")
  reviews = relationship("ReviewModel", back_populates="book")

  genre = Column(String, nullable=True)
  publication_year = Column(Integer, nullable=True)