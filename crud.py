from fastapi import FastAPI, HTTPException, Request, Depends, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

books = [
    {
        "id" : 1,
        "name": "Secret of piviot bosss",
        "author": "franck ochava",
        "release year" : 1901
    },
    {
        "id" : 2,
        "name": "Secret of piviot bosss",
        "author": "franck ochava",
        "release_year" : 1901
        },

    {
        "id" : 3,
        "name": "Eat the Frog",
        "author": "Brain Tracy",
         "release_year" : 1958
        },

    {
        "id" : 4,
        "name": "Inteligent Investors",
        "author": "Jd avans",
        "release_year" : 1951
        },

    {
        "id" : 5,
        "name": "Atomic habit",
        "author": "Lousiana",
        "release_year" : 1985
        },

    {
        "id" : 6,
        "name": "Think and grow rich",
        "author": "Nepolean hill",
        "release_year" : 2001
        },                
]


class BookModel(BaseModel):
    id: int
    name: str
    author: str
    release_year : int

class BookResponseModel(BaseModel):
    name: str
    author: str    


@app.get("/get_all_books")
def get_all_books():
    return {"books": books}

@app.post("/create_book", status_code=200)
def create_book(book: BookModel):
    new_book = book
    books.append(new_book)
    return {"message": "Book created successfully", "book": new_book}

@app.get("/get_one_book/{id}")
def get_book(id:int):
    for book in books:
        if book['id'] == id:
            return {"book": book}

    raise HTTPException(status_code = 400, detail="unable to create the book")

@app.patch("/update_book/{id}")
def update(id: int, book_model: BookResponseModel):
    for book in books:
        if book["id"] == id:
            book["name"] = book_model.name
            book["author"] = book_model.author
            return {"book" : book}
        
    raise HTTPException(status_code = 400, detail="unable to update the book")

@app.delete("/remove_book/{id}")
def remove_book(id:int):
    for book in books:
        if book['id'] == id:
            books.remove(book)
            return {"message": "Books deleted succesfully"}
    raise HTTPException(status_code = 400, detail="unable to delete the book")


