import uvicorn as uvicorn
from bson import ObjectId
from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from database import add_book, collection
from models import BookSchema

app = FastAPI()


@app.post('/book')
async def create(book: BookSchema = Body(...)):
    book = jsonable_encoder(book)
    new_book = add_book(book)
    return new_book


# Retrieve a student with a matching ID to delete
@app.delete("/book/{_id}")
async def remove(_id: str):
    book = collection.find_one({"_id": ObjectId(_id)})
    if book:
        collection.delete_one({"_id": ObjectId(_id)})
        return {"message": "Book deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@app.get('/books')
async def get_all_books():
    books = []
    for book in collection.find({}, {'_id': 0}):  # Exclude _id field from the response
        books.append(book)
    return jsonable_encoder({'books': books})





if __name__ == '__main__':
    uvicorn.run(app, port=6000)
