# Request sender code (request_sender.py)
import requests

def send_request_to_flask():
    # Define the URL of your Flask application endpoint
    url = 'http://127.0.0.1:5001/query'

    # Define the JSON data for your request
    query_search = str(input("Query Search: "))
    data = {'query': query_search}

    # Send a POST request to the Flask application
    response = requests.post(url, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response from the Flask application
        print(response.json())
    else:
        print('Error:', response.status_code)

if __name__ == '__main__':
    send_request_to_flask()
