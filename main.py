import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from pymongo import MongoClient

app = FastAPI()
client = TestClient(app)

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['BookFinder']
collection = db['Book']


# API endpoint to insert a new book
@app.post('/books')
async def insert_book(title: str, pub_date: str, author: str, rating: str, genre: str):
    book = {
        'title': title,
        'pub_date': pub_date,
        'author': author,
        'rating': rating,
        'genre': genre
    }
    result = collection.insert_one(book)
    return {'inserted_id': str(result.inserted_id)}


# GET API BY Title
@app.post('//books/<string:title>')
def get_book(title):
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
    for book in collection.find():
        books.append(book)
    return jsonable_encoder(books)
    # Return the results
    return jsonify({'books': books})


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, port=5000)
