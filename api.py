"""Module for Playtomic API."""

import requests
import logging
from typing import Optional, Dict
from endpoints import Tenant, Tournament

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)  # Set logging level globally


class PlaytomicClient:
    BASE_URL = "https://api.playtomic.io"

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate the user and retrieve access tokens."""
        logger.debug("Authenticating user.")
        auth_url = f"{self.BASE_URL}/v3/auth/login"
        payload = {"email": self.email, "password": self.password}
        headers = {"Content-Type": "application/json"}

        response = self._send_http_request(url=auth_url, method="POST", json=payload, headers=headers)
        data = response.json()
        self.access_token = data.get("access_token")
        self.refresh_token = data.get("refresh_token")
        logger.info("User authenticated successfully.")

    def _get_headers(self) -> Dict[str, str]:
        """Return headers with the authorization token."""
        if not self.access_token:
            return {
                "Content-Type": "application/json"
            }
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _send_http_request(self, url: str, method: str, json: Optional[Dict] = None, data: Optional[Dict] = None,
                           params: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """Send HTTP request to Playtomic server with error handling and logging."""
        logger.debug(f"Sending {method} request to {url}")
        try:
            response = self.session.request(method=method, url=url, json=json, data=data, params=params, headers=headers)
            logger.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise e

        return response

    def send_request(self, method: str, endpoint: str, payload: Optional[Dict] = None) -> Dict:
        """Send HTTP request to Playtomic server, with automatic token refresh if needed."""
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()

        # Try sending the request, refresh token if unauthorized
        try:
            response = self._send_http_request(url, method, json=payload, headers=headers)
        except requests.HTTPError as e:
            if e.response.status_code == 401:  # Unauthorized, token might be expired
                logger.warning("Access token expired. Refreshing token...")
                self._refresh_access_token()
                headers = self._get_headers()
                response = self._send_http_request(url, method, json=payload, headers=headers)
            else:
                raise e

        return response.json()

    def _refresh_access_token(self) -> None:
        """Refresh the authentication token if expired."""
        logger.debug("Refreshing access token.")
        refresh_url = f"{self.BASE_URL}/v3/auth/refresh"
        payload = {"refresh_token": self.refresh_token}
        headers = {"Content-Type": "application/json"}

        response = self._send_http_request(url=refresh_url, method="POST", json=payload, headers=headers)
        data = response.json()
        self.access_token = data.get("access_token")
        self.refresh_token = data.get("refresh_token")
        logger.info("Access token refreshed successfully.")

    # Tournament and Tenant operations
    def get_tournament(self, tournament_id: str) -> Dict:
        """Get tournament data."""
        tournament = Tournament(client=self)
        return tournament.get(tournament_id)

    def create_tournament(self, tournament_data: Dict) -> Dict:
        """Create a new tournament."""
        tournament = Tournament(client=self)
        return tournament.create(tournament_data)

    def get_tenant(self, tenant_id: str) -> Dict:
        """Get tenant information."""
        tenant = Tenant(client=self)
        return tenant.get(tenant_id)

    def create_tenant(self, tenant_data: Dict) -> Dict:
        """Create a new tenant."""
        tenant = Tenant(client=self)
        return tenant.create(tenant_data)
