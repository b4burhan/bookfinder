import json

import requests
from fastapi.testclient import TestClient

from BookFinderInFastApi import app  # assuming your FastAPI app is defined in a file called main.py

client = TestClient(app)


# Test insert a book to the database
def test_get_book_by_title():
    book = {
        "title": "The Great Gatsby",
        "pub_date": "1925",
        "author": "F. Scott Fitzgerald",
        "rating": "4.3",
        "genre": "Fiction"
    }
    response = client.post("/books", json=book)
    assert response.status_code == 200

    # Now, let's test getting the book by title
    response = client.get("/books/The Great Gatsby")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "Fiction",
        "pub_date": "1925",
        "rating": "4.3"
    }


# validate that the api return correct HTTP status code (e.g. 200) get request success
def test_get_books():
    response = requests.get('http://localhost:5000/books')
    assert response.status_code == 200


#  To test  Check data Formate is json or not
def test_get_books_by_keyword():
    response = requests.get('http://127.0.0.1:5000/booksbyKeyWord/?title=da')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert json.loads(response.text) is not None


#  test to ensure that the api return correct HTTP status code
def test_get_book_status_code():
    response = requests.get('http://localhost:5000/books/Python 101')
    assert response.status_code == 200
