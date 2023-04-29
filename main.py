import uvicorn as uvicorn
from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

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


# Get ALL
@app.get('/books')
async def get_all_books():
    books = []
    for book in collection.find({}, {'_id': 0}):  # Exclude _id field from the response
        books.append(book)
    return jsonable_encoder({'books': books})


# Get any related key word
@app.get('/BooksByKeyWord')
async def get_books_by_title(title: str):
    books = []
    for book in collection.find({'title': {'$regex': f'.*{title}.*', '$options': 'i'}}, {'_id': 0}):
        # Use $regex to perform a case-insensitive regex search for titles containing the given word
        books.append(book)
    return jsonable_encoder({'books': books})
# ?title=da

if __name__ == '__main__':
    uvicorn.run(app, port=5000)
