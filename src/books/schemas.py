from pydantic import BaseModel

class BookModel(BaseModel):
    id: int
    name: str
    author: str
    release_year : int

class BookResponseModel(BaseModel):
    name: str
    author: str 