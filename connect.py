from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['BookFinder']
collection = db['Book']


# Route to check the connection
# def check_connection():
#     data = collection.find_one()
#     if data:
#         print ('Connection successful')
#     else:
#         print('Connection failed')
#
# check_connection()



# API endpoints
@app.route('/books', methods=['GET'])
def get_books():
    # Get query parameters
    title = request.args.get('title')
    author = request.args.get('author')
    genre = request.args.get('genre')
    pub_date = request.args.get('pub_date')

    # Build the query
    query = {}
    if title:
        query['title'] = title
    if author:
        query['author'] = author
    if genre:
        query['genre'] = genre
    if pub_date:
        query['pub_date'] = pub_date

    # Query the database
    books = []
    for book in collection.find(query):
        books.append({
            'title': book['title'],
            'author': book['author'],
            'genre': book['genre'],
            'pub_date': book['pub_date'],
            'rating': book.get('rating', None)
        })

    # Return the results
    return jsonify({'books': books})


@app.route('/books/<string:title>', methods=['GET'])
def get_book(title):
    # Query the database
    book = collection.find_one({'title': title})

    if book:
        # Build the response
        response = {
            'title': book['title'],
            'author': book['author'],
            'genre': book['genre'],
            'pub_date': book['pub_date'],
            'rating': book.get('rating', None)
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Book not found'}), 404


@app.route('/books', methods=['POST'])
def add_book():
    # Parse the request data
    data = request.get_json()
    title = data.get('title', None)
    author = data.get('author', None)
    genre = data.get('genre', None)
    pub_date = data.get('pub_date', None)
    rating = data.get('rating', None)

    # Validate the data
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    # Insert the data into the database
    collection.insert_one({
        'title': title,
        'author': author,
        'genre': genre,
        'pub_date': pub_date,
        'rating': rating
    })

    # Build the response
    response = {
        'title': title,
        'author': author,
        'genre': genre,
        'pub_date': pub_date,
        'rating': rating
    }
    return jsonify(response), 201


if __name__ == '__main__':
    app.run(debug=True)
