from datetime import datetime

import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from bson.objectid import ObjectId

app = FastAPI()

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['BookFinder']
collection = db['Book']


# API endpoint to insert a new book
class Book(BaseModel):
    title: str
    pub_date: datetime
    author: str
    rating: int
    genre: str


# Post Request
@app.post('/books')
async def insert_book(book: Book):
    book = book.dict()
    result = collection.insert_one(book)
    return {'inserted_id': str(result.inserted_id)}


# API endpoint to update an existing book by its ID
@app.put('/books/{book_id}')
async def update_book(book_id: str, book: Book):
    # Convert the book object to a dict
    book_dict = jsonable_encoder(book)

    # Try to update the book with the given ID
    result = collection.update_one({'_id': ObjectId(book_id)}, {'$set': book_dict})
    if result.modified_count == 0:
        # If no book was updated, raise an HTTPException with a 404 status code
        raise HTTPException(status_code=404, detail='Book not found')
    else:
        # If a book was updated, return a success message with the updated book
        updated_book = collection.find_one({'_id': ObjectId(book_id)}, {'_id': 0})
        return jsonable_encoder({'message': 'Book updated successfully', 'book': updated_book})


# Get ALL Book
@app.get('/books')
async def get_all_books():
    books = []
    for book in collection.find({}, {'_id': 0}):  # Exclude _id field from the response
        books.append(book)
    return jsonable_encoder({'books': books})


# Get data by field and keyword
@app.get('/BooksByKeyWord')
async def get_books_by_title(field: str, keyword: str):
    # Define a dictionary to map query parameters to MongoDB field names
    field_mapping = {'title': 'title', 'pub_date': 'pub_date', 'author': 'author', 'rating': 'rating', 'genre': 'genre'}

    # Check if the provided field is valid
    if field not in field_mapping:
        return {'error': f'Invalid field "{field}". Valid fields are {", ".join(field_mapping.keys())}'}

    # Define the query to find documents containing the given keyword in the specified field
    query = {field_mapping[field]: {'$regex': f'.*{keyword}.*', '$options': 'i'}}

    # Use MongoDB's projection feature to retrieve only the required fields
    projection = {field_mapping[f]: 1 for f in field_mapping}
    projection['_id'] = 0

    # Find the matching documents in the database
    cursor = collection.find(query, projection)

    # Convert the MongoDB documents to dictionaries
    books = [{f: doc[f] for f in field_mapping} for doc in cursor]

    return {'books': books}


# define the route for deleting a book by id
@app.delete("/books/{book_id}")
async def delete_book_by_id(book_id: str):
    try:
        # check if the book with the given id exists
        book = collection.find_one({"_id": ObjectId(book_id)})
        if book:
            # delete the book by its ObjectId
            collection.delete_one({"_id": ObjectId(book_id)})
            return {"message": "Book deleted successfully"}
        else:
            # return 404 if book not found
            raise HTTPException(status_code=404, detail="Book not found")
    except:
        # return 500 if there is any server error
        raise HTTPException(status_code=500, detail="Server error")


if __name__ == '__main__':
    uvicorn.run(app, port=1000)
