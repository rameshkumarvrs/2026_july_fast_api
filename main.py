from fastapi import FastAPI, Request, HTTPException,status
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate, PostResponse
from typing import List

from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts = [
    {
        "id": 1,
        "author": "Corey Anderson",
        "title": "FastAPI learning way",
        "content": "This framework is really useful to learn and implement",
        "date_posted": "April 20 2025"
    },
    {
        "id": 2,
        "author": "Kane Williamson",
        "title": "Ruby on Rails dead nowadays",
        "content": "This framework is really useful to learn and implement",
        "date_posted": "May 20 2025"
    }
]


@app.get("/",  include_in_schema=False, name="home")
@app.get("/posts",  include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"},)


@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(post_id: int, request: Request):
    for post in posts:
        if post.get("id") == post_id:
            title = post['title'][:50]
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": title})
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="post not found")   
        


@app.get("/api/posts", response_model=List[PostResponse])
def get_posts():
    return posts


# ## Create Post
# @app.post(
#     "/api/posts",
#     response_model=PostResponse,
#     status_code=status.HTTP_201_CREATED,
# )
# def create_post(post: PostCreate):
#     new_id = max(p["id"] for p in posts) + 1 if posts else 1
#     new_post = {
#         "id": new_id,
#         "author": post.author,
#         "title": post.title,
#         "content": post.content,
#         "date_posted": "April 23, 2025",
#     }
#     posts.append(new_post)
#     return new_post






## Create Post code by ramesh

@app.post("/api/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) +1 if posts else 1
    new_post ={
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "April 25, 2025"
    }
    posts.append(new_post)
    return new_post


#This code for get the single post

@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post available")


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
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )

