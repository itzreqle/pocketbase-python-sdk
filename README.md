# PocketBase Python SDK

Welcome to the PocketBase Python SDK! This SDK simplifies the process of interacting with the PocketBase API, allowing you to manage collections, records, and authentication directly through Python.

## 🚀 Features

- **Authentication:** Securely connect with the PocketBase API using tokens.
- **CRUD Operations:** Create, read, update, and delete records in specified collections.
- **Dynamic Collections:** Easily interact with multiple collections.
- **Token Generation:** Generate tokens using username and password.
- **Filtering & Pagination:** Optional support for filtering and paginating results.
- **User Management:** Handle user verification, password resets, and email changes.
- **OAuth2 Provider Management:** Integrate with various OAuth2 providers.
- **Customizable Requests:** Tailor your request handling to fit your needs.

## 📋 Requirements

Before you begin, ensure you have the following:

- Python 3.8 or higher
- [requests](https://pypi.org/project/requests/) library
- A valid PocketBase instance URL

## 🔧 Installation

Follow these steps to install the PocketBase Python SDK:

1. **Clone the repository or download the source files:**
   ```bash
   git clone https://github.com/itzreqle/pocketbase-python-sdk.git
   ```

2. **Install required dependencies using pip:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in your project root with the following environment variables:**
   ```
   POCKETBASE_BASE_URL=https://your-pocketbase-instance.com
   POCKETBASE_COLLECTION=your_collection_name
   POCKETBASE_API_TOKEN=your_api_token
   ```

## 📚 Usage

### 1. Initialize the SDK

To start using the SDK, instantiate the `PocketBase` class:

```python
from pocketbase import PocketBase

pb = PocketBase()
```

### 2. Authentication

Authenticate users with various methods:

```python
# Password authentication
response = pb.auth_with_password('user@example.com', 'password123')

# OAuth2 authentication
response = pb.auth_with_oauth2_flow({'provider': 'google'})

# Refresh authentication
response = pb.refresh_auth()
```

### 3. CRUD Operations

Manage your records with ease:

```python
# Get all records
query_params = {'filter': 'status=active'}
response = pb.list_records(query_params=query_params, page=1, per_page=20)
print(response)

# Get record by ID
record_id = 'your-record-id'
response = pb.get_record(record_id)
print(response)

# Create a new record
data = {'name': 'New Item', 'description': 'A description of the item.'}
response = pb.create_record(data)
print(response)

# Update a record
record_id = 'your-record-id'
data = {'name': 'Updated Item Name'}
response = pb.update_record(record_id, data)
print(response)

# Delete a record
record_id = 'your-record-id'
response = pb.delete_record(record_id)
print(response)
```

### 4. User Management

Manage user accounts seamlessly:

```python
# Request email verification
response = pb.request_verification('user@example.com')

# Confirm email verification
response = pb.confirm_verification('verification_token')

# Request password reset
response = pb.request_password_reset('user@example.com')

# Confirm password reset
response = pb.confirm_password_reset('reset_token', 'new_password', 'new_password_confirm')
```

### 5. Generate and Set Token

Manage authentication tokens easily:

```python
# Generate a new token
username = 'your-username'
password = 'your-password'
response = pb.generate_token(username, password)
print(response)

# Manually set a new token
pb.set_token('your-new-token')
```

## ⚠️ Error Handling

All API responses are returned as dictionaries, including the status code and response data. For example:

```python
{
    'status_code': 200,
    'data': {
        'id': 'abc123',
        'name': 'Item Name',
        'created': '2023-01-01T12:00:00Z'
    }
}
```

In case of errors, the SDK will return an error message along with the HTTP status code.

## 🤝 Contributing

We welcome contributions! Feel free to submit a Pull Request to enhance the SDK.

## ❓ Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/itzreqle/pocketbase-python-sdk/issues).

## 📄 License

This project is licensed under the MIT License.
