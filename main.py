from fastapi import FastAPI

app = FastAPI()


@app.get("/display")
def view():
    return "Hello Rameshkumar"
