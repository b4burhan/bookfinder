from typing import Optional
import uvicorn as uvicorn
from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status

from database import add_book, retrieve_books, retrieve_book_id, delete_book
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
async def get_book_data(id):
    book = retrieve_book_id(id)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Resource not found')


@app.delete("/book/{id}")
async def delete_book_data(id: str):
    deleted_book = delete_book(id)
    if deleted_book:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Resource not found')


if __name__ == '__main__':
    uvicorn.run(app, port=6000)
