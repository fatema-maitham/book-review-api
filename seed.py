from sqlalchemy.orm import sessionmaker
from config.environment import DATABASE_URL
from sqlalchemy import create_engine

from models.base import Base

from models.user import UserModel
from models.book import BookModel
from models.review import ReviewModel

from data.user_data import user_list
from data.book_data import create_test_books_and_reviews


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


try:
    print("Recreating database...")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Seeding the database...")

    db = SessionLocal()

    # Add users first
    db.add_all(user_list)
    db.commit()

    # Add books and reviews
    books, reviews = create_test_books_and_reviews()

    db.add_all(books)
    db.commit()

    db.add_all(reviews)
    db.commit()

    db.close()

    print("Database seeding complete!")

except Exception as e:
    print("An error occurred:", e)