from typing import Optional
import uvicorn as uvicorn
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder

from database import add_book, retrieve_books, retrieve_book_id, delete_student
from models import BookSchema

app = FastAPI()


@app.post('/book')
async def create(book: BookSchema = Body(...)):
    book = jsonable_encoder(book)
    new_book = add_book(book)
    return new_book


@app.get('/book')
async def get_books(search: Optional[str] = None):
    books = retrieve_books(search)
    return books


@app.get("/book/{id}")
async def get_student_data(id):
    student = retrieve_book_id(id)
    if student:
        return student


@app.delete("/book/{id}")
async def delete_student_data(id: str):
    deleted_student = await delete_student(id)
    if deleted_student:
        return {"message": "Book deleted successfully"}
    return {"An error occurred", 404, "Student with id {0} doesn't exist".format(id)}


if __name__ == '__main__':
    uvicorn.run(app, port=6000)
