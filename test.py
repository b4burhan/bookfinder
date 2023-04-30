from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_book():
    book_data = {
        "title": "Test Book",
        "publish_date": "2022-01-01",
        "author": "Test Author",
        "rating": "4",
        "genre": "Test Genre"
    }
    response = client.post("/book", json=book_data)
    assert response.status_code == 200


def test_get_all_books():
    response = client.get("/book")
    assert response.status_code == 200
    assert response.json() is not None


def test_search_books():
    response = client.get("/book?search=Test")
    assert response.status_code == 200
    assert response.json() is not None

    deleted_book = collection.find_one({"_id": ObjectId(book_id)})
    assert deleted_book is None
