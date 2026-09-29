from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user

from models.book import BookModel

from serializers.book import (
    BookSchema,
    CreateBookSchema,
    UpdateBookSchema
)

router = APIRouter(tags=["Books"])


# CREATE BOOK
@router.post("/books", response_model=BookSchema, status_code=201)
def create_book(
    book: CreateBookSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_book = BookModel(
        title=book.title,
        author=book.author,
        description=book.description,
        user_id=current_user.id
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


# GET ALL BOOKS
@router.get("/books", response_model=list[BookSchema])
def get_books(db: Session = Depends(get_db)):
    books = db.query(BookModel).all()

    return books


# GET ONE BOOK
@router.get("/books/{book_id}", response_model=BookSchema)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# UPDATE BOOK
@router.put("/books/{book_id}", response_model=BookSchema)
def update_book(
    book_id: int,
    book: UpdateBookSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_book = db.query(BookModel).filter(
        BookModel.id == book_id
    ).first()

    if not existing_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Only the owner can update the book
    if existing_book.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own books"
        )

    existing_book.title = book.title
    existing_book.author = book.author
    existing_book.description = book.description

    db.commit()
    db.refresh(existing_book)

    return existing_book


# DELETE BOOK
@router.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_book = db.query(BookModel).filter(
        BookModel.id == book_id
    ).first()

    if not existing_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Only the owner can delete the book
    if existing_book.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own books"
        )

    db.delete(existing_book)
    db.commit()

    return {"message": "Book deleted successfully"}