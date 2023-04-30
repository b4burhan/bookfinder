from typing import Optional

import uvicorn as uvicorn
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder

from database import add_book, retrieve_books
from models import BookSchema

app = FastAPI()


@app.post('/book')
async def create(book: BookSchema = Body(...)):
    book = jsonable_encoder(book)
    new_book = add_book(book)
    return new_book


#
# @app.put('/books/{book_id}')
# async def update_book(book_id: str, book: Book):
#     book_dict = jsonable_encoder(book)
#     result = collection.update_one({'_id': ObjectId(book_id)}, {'$set': book_dict})
#     if result.modified_count == 0:
#         # If no book was updated, raise an HTTPException with a 404 status code
#         raise HTTPException(status_code=404, detail='Book not found')
#     else:
#         # If a book was updated, return a success message with the updated book
#         updated_book = collection.find_one({'_id': ObjectId(book_id)}, {'_id': 0})
#         return jsonable_encoder({'message': 'Book updated successfully', 'book': updated_book})
#
#
@app.get('/book')
async def get_books(search: Optional[str] = None):
    books = retrieve_books(search)
    return books


#
#
# @app.delete("/books/{book_id}")
# async def delete_book_by_id(book_id: str):
#     try:
#         # check if the book with the given id exists
#         book = collection.find_one({"_id": ObjectId(book_id)})
#         if book:
#             # delete the book by its ObjectId
#             collection.delete_one({"_id": ObjectId(book_id)})
#             return {"message": "Book deleted successfully"}
#         else:
#             # return 404 if book not found
#             raise HTTPException(status_code=404, detail="Book not found")
#     except:
#         # return 500 if there is any server error
#         raise HTTPException(status_code=500, detail="Server error")


if __name__ == '__main__':
    uvicorn.run(app, port=1000)
