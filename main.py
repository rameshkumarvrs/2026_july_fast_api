from fastapi import FastAPI

from pydantic import BaseModel
from typing import Optional


class items(BaseModel):
    name : str
    price : float
    availablity : Optional[bool] = None 

app = FastAPI()

emp = [
    {"name": 'ramesh', "id": 101, 'place': "Namakkal"},
     {"name": 'Haran', "id": 102, 'place': "Newzeland"},
      {"name": 'Riya', "id": 103, 'place': "karur"}
]

@app.post("/items")
def create_items(data : items):
    return {"messges": "items added successfully", "data": data}


@app.get("/display")
def view():
    return "Hello Rameshkumar"

@app.get("/display/{id}")
def display_id(id: int):
    return {"message": id}

@app.get("/employee/{id}")
def get_emp(id:int):
    for e in emp:
        if e["id"] == id:
            return e

@app.get("/employee")
def get_emp_det(id:int):
    for e in emp:
        if e['id'] == id:
            return e


