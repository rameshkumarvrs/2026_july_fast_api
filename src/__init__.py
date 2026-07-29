from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Response,Cookie

from src.books.routes import book_router

version = "v1"

app =FastAPI(
    version=version
)

app.include_router(book_router, prefix=f"/api/{version}/books")