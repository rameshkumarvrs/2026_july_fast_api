from fastapi import FastAPI

app = FastAPI()

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


@app.get("/")
def home():
    return {"message": "Hello world"}


@app.get("/api/posts")
def get_posts():
    return posts