from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Response,Cookie
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate, PostResponse, UserCreate, UserResponse
from typing_extensions import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)


app =FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")

templates = Jinja2Templates(directory="templates")





# posts = [
#     {
#         "id" : 1,
#         "name": "Secret of piviot bosss",
#         "title": "this book related to the stock market",
#         "author": "franck ochava",
#         "release year" : 1901
#     },
#     {
#         "id" : 2,
#         "name": "Secret of piviot bosss",
#         "title": "this book related to the stock market",
#         "author": "franck ochava",
#         "release_year" : 1901
#         },

#     {
#         "id" : 3,
#         "name": "Eat the Frog",
#         "title": "this book related to the personal growth",
#         "author": "Brain Tracy",
#          "release_year" : 1958
#         },

#     {
#         "id" : 4,
#         "name": "Inteligent Investors",
#         "title": "this book related to the personal growth",
#         "author": "Jd avans",
#         "release_year" : 1951
#         },

#     {
#         "id" : 5,
#         "name": "Atomic habit",
#         "title": "this book related to the personal growth",
#         "author": "Lousiana",
#         "release_year" : 1985
#         },

#     {
#         "id" : 6,
#         "name": "Think and grow rich",
#         "title": "this book related to the personal growth",
#         "author": "Nepolean hill",
#         "release_year" : 2001
#         },                
# ]


@app.get("/allposts")
def all_posts():
     return posts



@app.post(
          "/posts",
          response_model=PostResponse,
          status_code=201,
)
def create_posts(post:PostCreate):
     new_id = max(p["id"] for p in posts) + 1 if posts else 1
     new_post = {
          "id": new_id,
          "author": post.author,
          "title": post.title,
          "content": post.content,
          "date_posted": "April 28, 2026"
     }
     posts.append(new_post)
     return new_post





@app.get("/", name="home")
@app.get("/posts", name="posts")
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
     result = db.execute(
          select(models.Post)
     )
     posts = result.scalars().all()
     return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"},)


@app.get("/posts/{id}", include_in_schema=False, response_model=PostResponse)
def get_post(id: int, request: Request):
     for post in posts:
          if post.get("id") == id:
               title = post['title'][:50]
               return templates.TemplateResponse(request, "post.html", {"post": post, "title": title},)
     raise HTTPException(status_code=404, detail="the post is not available")   



@app.post("/users",response_model=UserResponse, status_code=201,)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
         select(models.User).where(models.User.username == user.username),
    )
    existing_user = result.scalars().first()

    if existing_user:
         raise HTTPException(status_code=400, detail="User name already exists",)


    result = db.execute(
         select(models.User).where(models.User.email == user.email),
    )

    existing_email = result.scalars().first()

    if existing_email:
         raise HTTPException(status_code=400, detail="User Email already exists")

    new_user = models.User(
         username= user.username,
         email = user.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
def get_user(user_id:int, db: Annotated[Session, Depends(get_db)]):
     result = db.execute(
          select(models.User).where(models.User.id == user_id),
     )

     user = result.scalars().first()

     if user:
          return user

     raise HTTPException(status_code=404, detail="User not found")



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