import os
import requests
from dotenv import load_dotenv

class PocketBase:
    def __init__(self, base_url=None, collection=None, token=None):
        # Load environment variables from .env file
        load_dotenv()

        # Set base URL, collection, and token from parameters or environment variables
        self.base_url = base_url or os.getenv('POCKETBASE_BASE_URL').rstrip('/')
        self.collection = collection or os.getenv('POCKETBASE_COLLECTION')
        self.token = token or os.getenv('POCKETBASE_API_TOKEN')

        # Error handling if any of these are missing
        if not self.base_url or not self.collection:
            raise ValueError("Base URL or Collection not found! Set POCKETBASE_BASE_URL and POCKETBASE_COLLECTION in the .env file.")
        if not self.token:
            raise ValueError("Token not found! Set POCKETBASE_API_TOKEN in the .env file.")

    def set_token(self, token):
        self.token = token

    def send_request(self, method, endpoint, data=None, query_params=None):
        url = f"{self.base_url}/api/collections/{self.collection}/{endpoint}"

        # Append query parameters to the URL
        if query_params:
            url += f"?{requests.compat.urlencode(query_params)}"

        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        # Send request using requests library
        response = requests.request(method, url, json=data, headers=headers)

        # Raise error if the request fails
        response.raise_for_status()
        return response.status_code, response.json()

    def generate_token(self, username, password):
        endpoint = f"{self.base_url}/api/admins/auth-with-password"
        data = {'identity': username, 'password': password}

        # Send POST request
        response = requests.post(endpoint, json=data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()

        result = response.json()
        if 'token' in result:
            self.set_token(result['token'])
            print(f"Generated Token: {result['token']}")
        else:
            print(f"Error generating token: {response.json()}")
        return result

    def get_all_records(self, query_params=None, page=1, per_page=20):
        query_params = query_params or {}
        query_params.update({'page': page, 'perPage': per_page})
        return self.send_request('GET', 'records', query_params=query_params)

    def get_record_by_id(self, record_id, query_params=None):
        return self.send_request('GET', f'records/{record_id}', query_params=query_params)

    def create_record(self, data):
        return self.send_request('POST', 'records', data=data)

    def update_record(self, record_id, data):
        return self.send_request('PATCH', f'records/{record_id}', data=data)

    def delete_record(self, record_id):
        return self.send_request('DELETE', f'records/{record_id}')
