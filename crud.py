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
            "id" : 1,
            "name": "Secret of piviot bosss",
            "author": "franck ochava",
            "release year" : 1901
        },

    {
            "id" : 2,
            "name": "Eat the Frog",
            "author": "Brain Tracy",
            "release year" : 1958
        },

    {
            "id" : 3,
            "name": "Inteligent Investors",
            "author": "Jd avans",
            "release year" : 1951
        },

    {
            "id" : 4,
            "name": "Atomic habit",
            "author": "Lousiana",
            "release year" : 1985
        },

    {
            "id" : 5,
            "name": "Think and grow rich",
            "author": "Nepolean hill",
            "release year" : 2001
        },                
]


@app.get("/get_all_books")
def get_all_books():
    return {"books": books}