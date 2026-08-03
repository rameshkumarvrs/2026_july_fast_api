from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Response,Cookie
from fastapi import Request
from fastapi.templating import Jinja2Templates

app =FastAPI()

templates = Jinja2Templates(directory="templates")

# class manf(BaseModel):
#     name : str
#     year : int


# class items(BaseModel):
#     name : str = Field(min_length = 2, max_length = 100)
#     price : float
#     availablity : Optional[bool] = None 
#     manufacturer : manf

# app = FastAPI()

# emp = [
#     {"name": 'ramesh', "id": 101, 'place': "Namakkal"},
#      {"name": 'Haran', "id": 102, 'place': "Newzeland"},
#       {"name": 'Riya', "id": 103, 'place': "karur"}
# ]

# @app.post("/items")
# def create_items(data : items):
#     return {"messges": "items added successfully", "data": data}


# @app.get("/display")
# def view():
#     return "Hello Rameshkumar"

# @app.get("/display/{id}")
# def display_id(id: int):
#     return {"message": id}

# @app.get("/employee/{id}")
# def get_emp(id:int):
#     for e in emp:
#         if e["id"] == id:
#             return e

# @app.get("/employee")
# def get_emp_det(id:int):
#     for e in emp:
#         if e['id'] == id:
#             return e


# @app.post("/feedback/")
# def get_feedback(name : str= Form(...), rating : int=Form(...), email: str = Form(...)):
#     return {
#         "status" : "form submited succesfully",
#         "name": name,
#         "email": email,
#         "rating": rating

#     }   


# @app.post("/file_upload/")
# async def get_file_details(file : UploadFile=File(...)):
#     content = await file.read()
#     try:
#         text_p = content.decode("utf-8")[:200]
#     except:
#         text_p = "unable to read the content"

#     return {
#          "filename": file.filename,
#          "content-type": file.content_type,
#          "Text": text_p
#      }  


# couname = "admin"
# copwd = "password"

# sessions ={}

# @app.post("/login")
# def login(uname: str, pwd: str, res: Response):
#     if couname == uname and copwd == pwd:
#        sid = str(uuid.uuid4())
#        sessions[sid] = {"username": uname}
#        res.set_cookie(key="sid", value=sid, httponly=True)
#        return {"msg": "login success", "sessions": sessions}

#     else:
#         raise HTTPException(status_code=404, detail= "Invalid credentials")


# @app.get("/home/")
# def home(sid :Optional[str]=Cookie(None)):
#     if sid is None or sid not in sessions:
#         raise HTTPException(status_code=401, detail="Not authenticated")

#     return {"user":sessions[sid]} 


posts = [
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


@app.get("/" )
@app.get("/posts")
def home(request: Request):
     return templates.TemplateResponse(request, "home.html", {"posts": posts})


