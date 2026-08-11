from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

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


@app.get("/api/posts")
def get_posts():
    return posts


#This code for get the single post

@app.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post

    return {"error": "post not found"}   

