import os
import requests
import secrets
import base64
import hashlib
from dotenv import load_dotenv

class PocketBase:
    """
    A client for interacting with PocketBase API.

    This class provides methods for basic CRUD operations and authentication.
    """

    def __init__(self, base_url=None, collection=None, token=None):
        """
        Initialize the PocketBaseClient.

        :param base_url: The base URL of the PocketBase instance. If not provided, loaded from environment.
        :param collection: The collection to interact with. If not provided, loaded from environment.
        :param token: The API token for authentication. If not provided, loaded from environment.
        """
        load_dotenv()

        self.base_url = base_url or os.getenv('POCKETBASE_BASE_URL', '').rstrip('/')
        self.collection = collection or os.getenv('POCKETBASE_COLLECTION')
        self.token = token or os.getenv('POCKETBASE_API_TOKEN')

        if not self.base_url:
            raise ValueError("Base URL not found! Please ensure POCKETBASE_BASE_URL is set in your .env file.")

        if not self.token:
            raise ValueError("Token not found! Please ensure POCKETBASE_API_TOKEN is set in your .env file.")

    def send_request(self, method, endpoint, data=None, query_params=None):
        """
        Send a request to the PocketBase API.

        :param method: HTTP method (GET, POST, PATCH, DELETE)
        :param endpoint: API endpoint
        :param data: Request payload (for POST and PATCH requests)
        :param query_params: Query parameters for the request
        :return: Dict containing status code and response data
        """
        url = f"{self.base_url}/{endpoint}"

        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        try:
            response = requests.request(
                method,
                url,
                json=data,
                params=query_params,
                headers=headers
            )
            response.raise_for_status()
            return {'status_code': response.status_code, 'data': response.json()}
        except requests.RequestException as e:
            return {'status_code': 500, 'data': {'error': f"Request error: {str(e)}"}}

    def set_token(self, token):
        """
        Set a new authentication token.

        :param token: The new token to use for authentication
        """
        self.token = token

    def generate_token(self, username, password):
        """
        Generate an admin authentication token.

        :param username: Admin username
        :param password: Admin password
        :return: Dict containing the generated token and user data
        """
        endpoint = "api/admins/auth-with-password"
        data = {
            'identity': username,
            'password': password
        }

        response = self.send_request('POST', endpoint, data)

        if response['status_code'] == 200 and 'token' in response['data']:
            token = response['data']['token']
            print(f"Generated Token: {token}")
            self.set_token(token)
            return response['data']
        else:
            print(f"Error generating token: {response['data']}")
            return response['data']

    def list_records(self, query_params=None, page=1, per_page=20):
        """
        List records from the current collection.

        :param query_params: Additional query parameters for filtering
        :param page: Page number for pagination (default: 1)
        :param per_page: Number of records per page (default: 20)
        :return: Dict containing status code and list of records
        """
        query_params = query_params or {}
        query_params.update({'page': page, 'perPage': per_page})
        endpoint = f"api/collections/{self.collection}/records"
        return self.send_request('GET', endpoint, query_params=query_params)

    def get_record(self, id, query_params=None):
        """
        Get a single record by ID.

        :param id: The ID of the record to retrieve
        :param query_params: Additional query parameters
        :return: Dict containing status code and record data
        """
        endpoint = f"api/collections/{self.collection}/records/{id}"
        return self.send_request('GET', endpoint, query_params=query_params)

    def create_record(self, data):
        """
        Create a new record in the current collection.

        :param data: Dict containing the data for the new record
        :return: Dict containing status code and created record data
        """
        endpoint = f"api/collections/{self.collection}/records"
        return self.send_request('POST', endpoint, data=data)

    def update_record(self, id, data):
        """
        Update an existing record.

        :param id: The ID of the record to update
        :param data: Dict containing the updated data for the record
        :return: Dict containing status code and updated record data
        """
        endpoint = f"api/collections/{self.collection}/records/{id}"
        return self.send_request('PATCH', endpoint, data=data)

    def delete_record(self, id):
        """
        Delete a record.

        :param id: The ID of the record to delete
        :return: Dict containing status code and deletion confirmation
        """
        endpoint = f"api/collections/{self.collection}/records/{id}"
        return self.send_request('DELETE', endpoint)

    def auth_with_password(self, identity, password, query_params=None):
        """
        Authenticate a user with their email/username and password.

        :param identity: User's email or username
        :param password: User's password
        :param query_params: Additional query parameters
        :return: Dict containing status code and authentication data
        """
        data = {
            'identity': identity,
            'password': password
        }
        endpoint = f"api/collections/{self.collection}/auth-with-password"
        return self.send_request('POST', endpoint, data, query_params)

    def auth_with_oauth2(self, params, query_params=None):
        """
        Authenticate a user using OAuth2.

        :param params: Dict containing OAuth2 parameters (provider, code, code_verifier, redirect_url)
        :param query_params: Additional query parameters
        :return: Dict containing status code and authentication data
        """
        required_params = ['provider', 'code', 'code_verifier', 'redirect_url']
        for param in required_params:
            if param not in params:
                raise ValueError(f"Missing required OAuth2 parameter: {param}")

        endpoint = f"api/collections/{self.collection}/auth-with-oauth2"
        return self.send_request('POST', endpoint, params, query_params)

    def auth_with_oauth2_flow(self, params):
        """
        Handle the complete OAuth2 authentication flow.

        :param params: Dict containing at least the 'provider' key
        :return: Dict containing status code and authentication data
        """
        if 'provider' not in params:
            raise ValueError("Missing required OAuth2 parameter: provider")

        code_verifier = secrets.token_urlsafe(32)
        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b'=').decode()

        redirect_url = f"{self.base_url}/api/oauth2-redirect"

        # Simulate receiving a code (in a real implementation, you'd redirect the user and handle the callback)
        code = "simulated_oauth2_code"

        return self.auth_with_oauth2({
            'provider': params['provider'],
            'code': code,
            'code_verifier': code_verifier,
            'redirect_url': redirect_url,
        })

    def refresh_auth(self, query_params=None):
        """
        Refresh the authentication token.

        :param query_params: Additional query parameters
        :return: Dict containing status code and refreshed authentication data
        """
        endpoint = f"api/collections/{self.collection}/auth-refresh"
        return self.send_request('POST', endpoint, query_params=query_params)

    def request_verification(self, email):
        """
        Request email verification for a user.

        :param email: Email address to verify
        :return: Dict containing status code and request confirmation
        """
        data = {'email': email}
        endpoint = f"api/collections/{self.collection}/request-verification"
        return self.send_request('POST', endpoint, data=data)

    def confirm_verification(self, token):
        """
        Confirm email verification.

        :param token: Verification token received in email
        :return: Dict containing status code and confirmation data
        """
        data = {'token': token}
        endpoint = f"api/collections/{self.collection}/confirm-verification"
        return self.send_request('POST', endpoint, data=data)

    def request_password_reset(self, email):
        """
        Request a password reset for a user.

        :param email: Email address of the user
        :return: Dict containing status code and request confirmation
        """
        data = {'email': email}
        endpoint = f"api/collections/{self.collection}/request-password-reset"
        return self.send_request('POST', endpoint, data=data)

    def confirm_password_reset(self, token, password, password_confirm):
        """
        Confirm and complete a password reset.

        :param token: Password reset token received in email
        :param password: New password
        :param password_confirm: Confirmation of the new password
        :return: Dict containing status code and confirmation data
        """
        data = {
            'token': token,
            'password': password,
            'passwordConfirm': password_confirm
        }
        endpoint = f"api/collections/{self.collection}/confirm-password-reset"
        return self.send_request('POST', endpoint, data=data)

    def request_email_change(self, new_email):
        """
        Request an email change for the authenticated user.

        :param new_email: New email address
        :return: Dict containing status code and request confirmation
        """
        data = {'newEmail': new_email}
        endpoint = f"api/collections/{self.collection}/request-email-change"
        return self.send_request('POST', endpoint, data=data)

    def confirm_email_change(self, token, password):
        """
        Confirm an email change request.

        :param token: Email change confirmation token received in email
        :param password: Current password of the user
        :return: Dict containing status code and confirmation data
        """
        data = {
            'token': token,
            'password': password
        }
        endpoint = f"api/collections/{self.collection}/confirm-email-change"
        return self.send_request('POST', endpoint, data=data)

    def list_auth_methods(self, query_params=None):
        """
        List all available authentication methods.

        :param query_params: Additional query parameters
        :return: Dict containing status code and list of auth methods
        """
        endpoint = f"api/collections/{self.collection}/auth-methods"
        return self.send_request('GET', endpoint, query_params=query_params)

    def list_external_auths(self, user_id, query_params=None):
        """
        List all external authentications for a user.

        :param user_id: ID of the user
        :param query_params: Additional query parameters
        :return: Dict containing status code and list of external auths
        """
        endpoint = f"api/collections/{self.collection}/records/{user_id}/external-auths"
        return self.send_request('GET', endpoint, query_params=query_params)

    def unlink_external_auth(self, user_id, provider):
        """
        Unlink an external authentication from a user.

        :param user_id: ID of the user
        :param provider: Name of the external auth provider to unlink
        :return: Dict containing status code and unlinking confirmation
        """
        endpoint = f"api/collections/{self.collection}/records/{user_id}/external-auths/{provider}"
        return self.send_request('DELETE', endpoint)
