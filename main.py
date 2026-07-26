from fastapi import FastAPI

app = FastAPI()


@app.get("/display")
def view():
    return "Hello Rameshkumar"

@app.get("/display/{id}")
def display_id(id: int):
    return {"message": id}
