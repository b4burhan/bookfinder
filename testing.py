# import pytest
# pytest testing.py
from fastapi.testclient import TestClient

from BookFinderInFastApi import app

client = TestClient(app)


# Test POST endpoint for inserting a new book
def test_insert_book():
    book_data = {
        "title": "Test Book",
        "pub_date": "2022-01-01",
        "author": "Test Author",
        "rating": "4",
        "genre": "Test Genre"
    }
    response = client.post("/books", json=book_data)
    assert response.status_code == 200
    assert response.json().get("inserted_id") is not None


# Test GET endpoint for retrieving a book by title
def test_get_book():
    book_title = "Test Book"
    response = client.get(f"/books/{book_title}")
    assert response.status_code == 200
    assert response.json().get("title") == book_title


# Test GET endpoint for retrieving all books
def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json().get("books") is not None
