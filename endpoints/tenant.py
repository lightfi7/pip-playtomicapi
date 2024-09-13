from ..api import PlaytomicClient


class Tenant:
    def __init__(self, client: PlaytomicClient) -> None:
        self.client = client

    def get(self, tenant_id):
        """Fetch tenant details by tenant ID."""
        endpoint = f"/v1/tenants/{tenant_id}"
        return self.client.send_request("GET", endpoint)

    def create(self, tenant_data):
        """Create a new tenant."""
        endpoint = "/v2/tenants"
        return self.client.send_request("POST", endpoint, payload=tenant_data)