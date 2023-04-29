import uvicorn as uvicorn
from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from pydantic import BaseModel

# from .main import app


app = FastAPI()

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['BookFinder']
collection = db['Book']


# API endpoint to insert a new book
class Book(BaseModel):
    title: str
    pub_date: str
    author: str
    rating: str
    genre: str


@app.post('/books')
async def insert_book(book: Book):
    book = book.dict()
    result = collection.insert_one(book)
    return {'inserted_id': str(result.inserted_id)}


# GET API BY Title
@app.get('/books/{title}')
def get_book(title: str):
    # Query the database
    book = collection.find_one({'title': title})

    if book:
        # Build the response
        response = {
            'title': book['title'],
            'author': book['author'],
            'genre': book['genre'],
            'pub_date': book['pub_date'],
            'rating': book.get('rating', None)
        }
        return jsonable_encoder(response)
    else:
        return jsonable_encoder({'error': 'Book not found'}), 404


@app.get('/books')
async def get_all_books():
    books = []
    for book in collection.find({}, {'_id': 0}):  # Exclude _id field from the response
        books.append(book)
    return jsonable_encoder({'books': books})


if __name__ == '__main__':
    uvicorn.run(app, port=5000)
