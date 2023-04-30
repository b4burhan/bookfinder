# BookStore API
This API allows users to query a MongoDB database to search for books by title, and also insert new books into the database.

# Requirements
To run this code, you will need:

Python 3.7+
FastAPI
pymongo


## Setup Locally

Clone the repository to your local machine and install requirements.

```bash
  pip install -r requirements.txt

```
Run development server.
```bash
  python main.py
```

## Running Tests
To run tests, run the following command in root folder
```bash
  pytest test.py
```

## API Endpoints

The following endpoints are available:

GET /books
Returns a list of all books in the database.

GET /books/{title}
Returns details for a book with a specific title.

POST /books
Adds a new book to the database.

Example Request/Response



# Contributors
This project was created by [Your Name]. Contributions are welcome - please submit a pull request if you would like to make changes.

