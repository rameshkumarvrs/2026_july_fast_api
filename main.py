from fastapi import FastAPI, Request

from fastapi.templating import Jinja2Templates

app = FastAPI()
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


@app.get("/",  include_in_schema=False)
@app.get("/posts",  include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request, "home.html")


@app.get("/api/posts")
def get_posts():
    return posts