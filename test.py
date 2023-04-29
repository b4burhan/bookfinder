import json
import concurrent.futures
import requests
from fastapi.testclient import TestClient
import time
import threading
from BookFinderInFastApi import app  # assuming your FastAPI app is defined in a file called main.py

client = TestClient(app)


# validate that the api return correct HTTP status code (e.g. 200) get request success
def test_get_books_validate():
    response = requests.get('http://localhost:5000/books')
    assert response.status_code == 200


#  To test  Check data Formate is json or not
def test_get_books_by_keyword():
    response = requests.get('http://127.0.0.1:5000/booksbyKeyWord/?title=da')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert json.loads(response.text) is not None


#  test to ensure that the api return correct HTTP status code
def test_get_book_status_code():
    response = requests.get('http://localhost:5000/books/Python 101')
    assert response.status_code == 200


# Define the number of concurrent requests to make
def test_concurrent_requests():
    num_requests = 10

    # Define a function to send a request to the API
    def send_request():
        response = requests.get('http://localhost:5000/books')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        assert len(response.json()['books']) > 0

    # Use the concurrent.futures module to send concurrent requests
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]

    # Ensure that all requests were successful and the data is consistent
    for future in futures:
        assert future.result() is None


# Test GET method for Books endpoint
def test_get_book_test():
    response = requests.get('http://localhost:5000/books')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert len(json.loads(response.text)['books']) > 0


# Number of concurrent users
num_users = 100

# Number of requests per user
num_requests_per_user = 10

# Endpoint to test
endpoint = 'http://localhost:5000/books'


# Function to simulate a user making requests
def make_requests():
    for key in range(num_requests_per_user):
        # Send a GET request to the endpoint
        response = requests.get(endpoint)
        # Ensure the API returns a 200 status code
        assert response.status_code == 200
        # Ensure the API returns data in JSON format
        assert response.headers['Content-Type'] == 'application/json'


# Start the timer
start_time = time.time()

# Create threads to simulate concurrent users
threads = []
for i in range(num_users):
    thread = threading.Thread(target=make_requests)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Calculate the total time taken
total_time = time.time() - start_time

# Print the results
print(f'Total time taken: {total_time} seconds')
print(f'Requests per second: {num_users * num_requests_per_user / total_time}')


def test_special_characters():
    # Send a POST request to the API with special characters in the data
    headers = {'Content-Type': 'application/json'}
    data = {"title": "Book with special characters!@#$%^&*()", "author": "Author with special characters!@#$%^&*()",
            "genre": "Genre with special characters!@#$%^&*()", "pub_date": "2022", "rating": "5.0"}
    response = requests.post('http://127.0.0.1:5000/books', headers=headers, data=json.dumps(data))

    # Ensure the API returns data in JSON format
    assert response.headers['Content-Type'] == 'application/json'

    # Ensure the API returns a 200 status code
    assert response.status_code == 200
