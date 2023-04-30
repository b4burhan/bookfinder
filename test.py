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

# def test_delete_book_by_id():
#     # create a book to delete
#     book = {"title": "Test Book", "author": "John Doe"}
#     inserted_book = collection.insert_one(book)
#     book_id = str(inserted_book.inserted_id)
#
#     # delete the book
#     response = client.delete(f"/books/{book_id}")
#
#     # verify that the book is deleted
#     assert response.status_code == 200
#     assert response.json() == {"message": "Book deleted successfully"}
#
#     deleted_book = collection.find_one({"_id": ObjectId(book_id)})
#     assert deleted_book is None
