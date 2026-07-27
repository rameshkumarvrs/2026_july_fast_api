from fastapi import FastAPI, Form, File, UploadFile, HTTPException

from pydantic import BaseModel, Field
from typing import Optional
import uuid

class manf(BaseModel):
    name : str
    year : int


class items(BaseModel):
    name : str = Field(min_length = 2, max_length = 100)
    price : float
    availablity : Optional[bool] = None 
    manufacturer : manf

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


@app.post("/feedback/")
def get_feedback(name : str= Form(...), rating : int=Form(...), email: str = Form(...)):
    return {
        "status" : "form submited succesfully",
        "name": name,
        "email": email,
        "rating": rating

    }   


@app.post("/file_upload/")
async def get_file_details(file : UploadFile=File(...)):
    content = await file.read()
    try:
        text_p = content.decode("utf-8")[:200]
    except:
        text_p = "unable to read the content"

    return {
         "filename": file.filename,
         "content-type": file.content_type,
         "Text": text_p
     }  


couname = "admin"
copwd = "password"

sessions ={}

@app.post("/login")
def login(uname: str, pwd: str):
    if couname == uname and copwd == pwd:
       sid = uuid.uuid4()
       return {"sid": sid}

    else:
        raise HTTPException(status_code=404, detail= "Invalid credentials")


