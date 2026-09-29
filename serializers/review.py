from pydantic import BaseModel


class ReviewSchema(BaseModel):
    id: int
    rating: int
    comment: str | None
    book_id: int
    user_id: int

    class Config:
        orm_mode = True


class CreateReviewSchema(BaseModel):
    rating: int
    comment: str | None = None


class UpdateReviewSchema(BaseModel):
    rating: int
    comment: str | None = None