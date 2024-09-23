# PocketBase Python SDK

This Python SDK provides an easy way to interact with the PocketBase API, allowing you to manage collections, records, and authentication directly through Python.

## Features
- Authentication with PocketBase API using tokens
- CRUD operations on records in specified collections
- Dynamic interaction with multiple collections
- Supports token generation using username and password
- Optional filtering and pagination support

## Requirements
- Python 3.6 or higher
- [requests](https://pypi.org/project/requests/) library for making HTTP requests
- A valid PocketBase instance URL
- Environment variables for configuration

## Installation

1. Install the required dependencies using `pip`:

```bash
pip install requests python-dotenv
```

2. Place the `PocketBase.py` file into your project directory.

3. Create a `.env` file in your project root with the following environment variables:

```
POCKETBASE_BASE_URL=https://your-pocketbase-instance.com
POCKETBASE_COLLECTION=your_collection_name
POCKETBASE_API_TOKEN=your_api_token
```

## Usage

### 1. Initialize the SDK

You can instantiate the `PocketBase` class by providing the PocketBase instance URL, collection name, and token. If these values are not provided, they will be loaded from the `.env` file.

```python
from PocketBase import PocketBase

pocketbase = PocketBase()
```

### 2. Get All Records

Retrieve all records from the current collection. You can also filter results and paginate them.

```python
query_params = {'filter': 'status=active'}
response = pocketbase.get_all_records(query_params, page=1, per_page=20)

print(response)
```

### 3. Get Record by ID

Retrieve a specific record by its ID from the collection.

```python
record_id = 'your-record-id'
response = pocketbase.get_record_by_id(record_id)

print(response)
```

### 4. Create a New Record

Add a new record to the collection by passing the data dictionary.

```python
data = {
    'name': 'New Item',
    'description': 'A description of the item.'
}

response = pocketbase.create_record(data)

print(response)
```

### 5. Update a Record

Update an existing record by its ID with the new data.

```python
record_id = 'your-record-id'
data = {
    'name': 'Updated Item Name'
}

response = pocketbase.update_record(record_id, data)

print(response)
```

### 6. Delete a Record

Delete a record from the collection by its ID.

```python
record_id = 'your-record-id'
response = pocketbase.delete_record(record_id)

print(response)
```

### 7. Generate a Token

Generate a new token using username and password authentication.

```python
username = 'your-username'
password = 'your-password'
response = pocketbase.generate_token(username, password)

print(response)
```

### 8. Set a New Token

Manually set a new token for the SDK, for example, after generating a new token.

```python
pocketbase.set_token('your-new-token')
```

## Error Handling

All responses from the API are returned as tuples with the status code and the decoded JSON response.

Example response:

```python
(200, {
    'id': 'abc123',
    'name': 'Item Name',
    'created': '2023-01-01T12:00:00Z'
})
```

In case of errors, the SDK will return an error message and the HTTP status code.

## License

This project is licensed under the MIT License.
