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


def test_delete_book_by_id():
    book = {
        "title": "Test Book", "author": "John Doe", "publish_date": "2019-10-12",
        "rating": 4,
        "genre": "programming"
    }
    response = client.post("/book", json=book)
    book_id = str(response.json().get('id'))
    response = client.delete(f"/book/{book_id}")
    assert response.status_code == 200


def test_data_format():
    book = {
        "title": "Test Book", "author": "John Doe", "publish_date": "2019-10-12",
        "rating": 4,
        "genre": "programming"
    }
    response = client.post("/book", json=book)
    book_id = str(response.json().get('id'))
    response = client.get(f"/book/{book_id}")
    assert response.headers["Content-Type"] == "application/json"
    assert isinstance(response.json(), dict)
