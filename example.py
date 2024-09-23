# Create an instance of the PocketBase client
pb = PocketBase()

# Generate token using username and password
pb.generate_token("your_username", "your_password")

# Get all records from the current collection
status_code, records = pb.get_all_records(page=1, per_page=20)
print(records)

# Get a specific record by ID
status_code, record = pb.get_record_by_id("some_record_id")
print(record)

# Create a new record
data = {"field": "value"}
status_code, new_record = pb.create_record(data)
print(new_record)

# Update an existing record
updated_data = {"field": "new_value"}
status_code, updated_record = pb.update_record("some_record_id", updated_data)
print(updated_record)

# Delete a record
status_code, deleted_record = pb.delete_record("some_record_id")
print(deleted_record)
