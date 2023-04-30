import pytest
import json
from fastapi.testclient import TestClient

from .database import  collection
from bson.objectid import ObjectId

client = TestClient(app)


# Create an automated test and test if the API correctly handles different HTTP methods (GET, POST, PUT, DELETE)
# for each endpoint and returns appropriate status codes and responses for each method.
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


# Test GET endpoint for retrieving all books
def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json().get("books") is not None


# Delete endpoint api test

def test_delete_book_by_id():
    # create a book to delete
    book = {"title": "Test Book", "author": "John Doe"}
    inserted_book = collection.insert_one(book)
    book_id = str(inserted_book.inserted_id)

    # delete the book
    response = client.delete(f"/books/{book_id}")

    # verify that the book is deleted
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}

    deleted_book = collection.find_one({"_id": ObjectId(book_id)})
    assert deleted_book is None
