from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Response,Cookie
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app =FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

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
        "title": "this book related to the stock market",
        "author": "franck ochava",
        "release year" : 1901
    },
    {
        "id" : 2,
        "name": "Secret of piviot bosss",
        "title": "this book related to the stock market",
        "author": "franck ochava",
        "release_year" : 1901
        },

    {
        "id" : 3,
        "name": "Eat the Frog",
        "title": "this book related to the personal growth",
        "author": "Brain Tracy",
         "release_year" : 1958
        },

    {
        "id" : 4,
        "name": "Inteligent Investors",
        "title": "this book related to the personal growth",
        "author": "Jd avans",
        "release_year" : 1951
        },

    {
        "id" : 5,
        "name": "Atomic habit",
        "title": "this book related to the personal growth",
        "author": "Lousiana",
        "release_year" : 1985
        },

    {
        "id" : 6,
        "name": "Think and grow rich",
        "title": "this book related to the personal growth",
        "author": "Nepolean hill",
        "release_year" : 2001
        },                
]


@app.get("/", name="home")
@app.get("/posts", name="posts")
def home(request: Request):
     return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"},)


@app.get("/posts/{id}", include_in_schema=False)
def get_post(id: int, request: Request):
     for post in posts:
          if post.get("id") == id:
               title = post['title'][:50]
               return templates.TemplateResponse(request, "post.html", {"post": post, "title": title},)
     raise HTTPException(status_code=404, detail="the post is not available")   



## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=422,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code":422,
            "title": "422 HTTP_422_UNPROCESSABLE_CONTENT",
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=422,
    )