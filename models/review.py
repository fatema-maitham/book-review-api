from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class ReviewModel(BaseModel):
    __tablename__ = "reviews"

    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)

    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=True)
    
    book = relationship("BookModel", back_populates="reviews")
    user = relationship("UserModel", back_populates="reviews")