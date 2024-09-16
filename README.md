# Playtomic API Python Client

This Python library provides a convenient way to interact with the Playtomic API, allowing you to authenticate, retrieve tenant details, create tournaments, and more. It automatically handles authentication and token refreshes for smooth API interactions.

## Features

- **Authentication**: Authenticate users with email and password.
- **Token Management**: Automatically refreshes access tokens when they expire.
- **Tenant Management**: Fetch tenant details.
- **Tournament Management**: Create and fetch tournaments.
- **Error Handling**: Proper error handling for HTTP requests and API failures.
- **Logging**: Detailed logging for easy debugging.

## Requirements

- Python 3.7+
- `requests` library

## Installation

You can install the required dependencies using `pip`:

```bash
pip install requests
```

## Usage

### 1. **Initialization**

First, you need to create an instance of the `PlaytomicClient` by providing your Playtomic credentials (email and password). This client will handle all interactions with the API.

```python
from playtomicapi import PlaytomicClient

# Initialize the client with your Playtomic credentials
client = PlaytomicClient(email="your_email@example.com", password="your_password")
```

### 2. **Fetching Tenant Information**

To fetch details about a tenant, use the `get_tenant` method. You need to provide the tenant ID as a parameter.

```python
tenant_id = "your_tenant_id"

tenant_info = client.Tenant.get(tenant_id)
print("Tenant Info:", tenant_info)
```

### 3. **Creating a New Tournament**

You can create a tournament by passing the tournament data to the `create_tournament` method.

```python

# Create a new tournament
tournament_data = {
    "name": "New Tournament",
    "start_date": "2024-09-13T23:00:00Z",
    "end_date": "2024-09-14T00:00:00Z"
}

new_tournament = client.Tournament.create(tournament_data)
print("Created Tournament:", new_tournament)
```

### 4. **Handling Access Token Expiration**

The `PlaytomicClient` automatically handles token expiration. If the access token expires, it will refresh the token and retry the request. You don’t need to manually refresh the token.

### Example Code:

```python
from playtomicapi.api import PlaytomicClient

# Initialize the Playtomic client with credentials
client = PlaytomicClient(email="user@example.com", password="password")

# Fetch a tenant's details
tenant_id = "123456789"
tenant_info = client.Tenant.get(tenant_id)
print(f"Tenant Info: {tenant_info}")


# Create a new tournament
tournament_data = {
    "name": "New Tournament",
    "start_date": "2024-09-13T23:00:00Z",
    "end_date": "2024-09-14T00:00:00Z"
}

new_tournament = client.Tournament.create(tournament_data)
print(f"Created Tournament: {new_tournament}")
```

## Endpoints

### `TournamentEndpoint`

#### `get(tournament_id: str) -> dict`
Fetches details for a specific tournament by ID.

#### `create(tournament_data: dict) -> dict`
Creates a new tournament with the provided tournament data.

### `TenantEndpoint`

#### `get(tenant_id: str) -> dict`
Fetches details for a specific tenant by ID.

#### `create(tenant_data: dict) -> dict`
Creates a new tournament with the provided tenant data.


## Logging

This library uses Python's `logging` module for detailed debugging. The default log level is set to `DEBUG` for verbose output. You can configure the logging level in your code:

```python
import logging
logging.basicConfig(level=logging.INFO)  # Change to INFO, WARNING, ERROR as needed
```

## Error Handling

The `PlaytomicClient` raises exceptions for HTTP errors using `requests.raise_for_status()`. You should handle exceptions appropriately in your application code. Here's a basic example:

```python
try:
    tenant_info = client.Tenant.get("tenant_id")
except requests.HTTPError as e:
    print(f"An error occurred: {e}")
```

## Contributing

If you wish to contribute to the project, feel free to submit issues or pull requests. Before contributing, ensure that your code follows Python's PEP 8 style guide and that all tests pass.

## License

This project is licensed under the MIT License.
