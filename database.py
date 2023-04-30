from pymongo import MongoClient, ReturnDocument
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['BookFinder']
collection = db['Book']


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


def retrieve_books(search):
    books = []
    filter = {'$or': [{'title': {'$regex': search}}, {'author': {'$regex': search}}, {'genre': {'$regex': search}}]}
    queryset = collection.find(filter) if search else collection.find()
    for book in queryset:
        books.append(book_helper(book))

    return books


def retrieve_book_id(id: str) -> dict:
    book = collection.find_one({"_id": ObjectId(id)})
    if book:
        return book_helper(book)


def delete_book(id: str):
    collection.delete_one({"_id": ObjectId(id)})
    return True


def update_book(id: str, data: dict):
    updated_book = collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": data},
                                                  return_document=ReturnDocument.AFTER)
    return book_helper(updated_book)
