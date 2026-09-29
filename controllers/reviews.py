from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user

from models.book import BookModel
from models.review import ReviewModel

from serializers.review import (
    ReviewSchema,
    CreateReviewSchema,
    UpdateReviewSchema
)

router = APIRouter(tags=["Reviews"])


# CREATE REVIEW
@router.post("/books/{book_id}/reviews", response_model=ReviewSchema, status_code=201)
def create_review(
    book_id: int,
    review: CreateReviewSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    new_review = ReviewModel(
        rating=review.rating,
        comment=review.comment,
        book_id=book_id,
        user_id=current_user.id
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


# GET ALL REVIEWS FOR A BOOK
@router.get("/books/{book_id}/reviews", response_model=list[ReviewSchema])
def get_book_reviews(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    reviews = db.query(ReviewModel).filter(
        ReviewModel.book_id == book_id
    ).all()

    return reviews


# GET ONE REVIEW
@router.get("/reviews/{review_id}", response_model=ReviewSchema)
def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    review = db.query(ReviewModel).filter(
        ReviewModel.id == review_id
    ).first()

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review


# UPDATE REVIEW
@router.put("/reviews/{review_id}", response_model=ReviewSchema)
def update_review(
    review_id: int,
    review: UpdateReviewSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_review = db.query(ReviewModel).filter(
        ReviewModel.id == review_id
    ).first()

    if not existing_review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    # Only the review owner can update it
    if existing_review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own reviews"
        )

    existing_review.rating = review.rating
    existing_review.comment = review.comment

    db.commit()
    db.refresh(existing_review)

    return existing_review


# DELETE REVIEW
@router.delete("/reviews/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_review = db.query(ReviewModel).filter(
        ReviewModel.id == review_id
    ).first()

    if not existing_review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    # Only the review owner can delete it
    if existing_review.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own reviews"
        )

    db.delete(existing_review)
    db.commit()

    return {"message": "Review deleted successfully"}