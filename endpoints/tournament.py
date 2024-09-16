from typing import Dict
from ..api import PlaytomicClient


class TournamentEndpoint:
    def __init__(self, client: PlaytomicClient) -> None:
        self.client = client

    def get(self, tournament_id: str):
        """Get tournament data."""
        endpoint = f"/v2/tournaments/{tournament_id}"
        return self.client.send_request("GET", endpoint)

    def create(self, tournament_data):
        """Create a new tournament."""
        endpoint = "/v2/tournaments"
        return self.client.send_request("POST", endpoint, payload=tournament_data)
