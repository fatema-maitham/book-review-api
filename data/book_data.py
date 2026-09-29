from models.book import BookModel
from models.review import ReviewModel


def create_test_books_and_reviews():

    book1 = BookModel(
        title="The Silent Patient",
        author="Alex Michaelides",
        description="A psychological mystery.",
        user_id=1
    )

    book2 = BookModel(
        title="Dracula",
        author="Bram Stoker",
        description="A classic gothic horror novel.",
        user_id=2
    )

    book3 = BookModel(
        title="Dune",
        author="Frank Herbert",
        description="A science fiction novel.",
        user_id=3
    )

    review1 = ReviewModel(
        rating=5,
        comment="Amazing book!",
        book_id=1,
        user_id=2
    )

    review2 = ReviewModel(
        rating=4,
        comment="Really interesting.",
        book_id=1,
        user_id=3
    )

    review3 = ReviewModel(
        rating=5,
        comment="A classic.",
        book_id=2,
        user_id=1
    )

    return [book1, book2, book3], [review1, review2, review3]