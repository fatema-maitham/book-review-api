from pydantic import BaseModel

class BookSchema(BaseModel):
  id: int
  title: str
  author: str
  description: str | None
  user_id: int

  class Config:
    orm_mode: True


class CreateBookSchema(BaseModel):
    title: str
    author: str
    description: str | None = None


class UpdateBookSchema(BaseModel):
    title: str
    author: str
    description: str | None = None