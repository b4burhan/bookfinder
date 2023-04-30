from typing import Optional
from fastapi import HTTPException
import uvicorn as uvicorn
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder

from database import add_book, retrieve_books, retrieve_book_id, delete_book, update_book
from models import BookSchema, ResponseModel, ErrorResponseModel, UpdateBookModel

app = FastAPI()


@app.post('/book')
async def create(book: BookSchema = Body(...)):
    book = jsonable_encoder(book)
    new_book = add_book(book)
    if new_book:
        return new_book
    else:
        return HTTPException(status_code=404, detail="Book Not Posted")


@app.get('/book')
async def get_books(search: Optional[str] = None):
    book = retrieve_books(search)
    if book:
        return book


@app.get("/book/{id}")
async def get_student_data(id):
    book = retrieve_book_id(id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/book/{id}")
async def delete_student_data(id: str):
    deleted_student = delete_book(id)
    if deleted_student:
        return HTTPException(status_code=200, detail="Book deleted successfully")
    else:
        return {"An error occurred", 404, "BooK with id {0} doesn't exist".format(id)}


@app.put("/book/{id}")
def update_student_data(id: str, req: UpdateBookModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_book = update_book(id, req)
    if updated_book:
        return updated_book
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


if __name__ == '__main__':
    uvicorn.run(app, port=1000)
