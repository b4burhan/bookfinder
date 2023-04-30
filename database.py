from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['bookstore']
collection = db['book']


def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "publish_date": book["publish_date"],
        "rating": book["rating"],
        "genre": book["genre"],
    }


def add_book(book_data: dict) -> dict:
    book = collection.insert_one(book_data)
    new_book = collection.find_one({"_id": book.inserted_id})
    return book_helper(new_book)
