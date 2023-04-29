BookFinder API
This API allows users to query a MongoDB database to search for books by title, and also insert new books into the database.

Requirements
To run this code, you will need:

Python 3.7+
FastAPI
pymongo

Installation
Clone the repository to your local machine.
Install the required packages using pip install -r requirements.txt.
Start the server by running python app.py.
API Endpoints
The following endpoints are available:

GET /books
Returns a list of all books in the database.

GET /books/{title}
Returns details for a book with a specific title.

POST /books
Adds a new book to the database.

Example Request/Response
Request:
bash
Copy code
POST /books
{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "pub_date": "1925",
    "rating": "5",
    "genre": "Fiction"
}
Response:
json
Copy code
{
    "inserted_id": "60935703386188365f738a75"
}

Testing
To run tests, run pytest from the root directory of the project. Tests are located in the tests/ directory.

Contributors
This project was created by [Your Name]. Contributions are welcome - please submit a pull request if you would like to make changes.