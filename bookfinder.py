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

# API endpoint to retrieve a book by its title and publication date
@app.route('/books/<string:title>/<string:pub_date>', methods=['GET'])
def get_book(title, pub_date):
    book = collection.find_one({'title': title, 'pub_date': pub_date})
    if book:
        return jsonify(book)
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