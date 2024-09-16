"""Module for Playtomic API."""

import requests
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)  # Set logging level globally


class Client:
    BASE_URL = "https://api.playtomic.io"

    def __init__(self, email: str, password: str) -> None:
        """
        Initialize the Playtomic client with authentication.

        :param str email: The email of the user.
        :param str password: The password of the user.
        """
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self._authenticate()

    def _authenticate(self) -> None:
        """
        Authenticate the user and retrieve access tokens.

        This method authenticates the user by sending a POST request with the provided email and password. 
        It stores the access token and refresh token for further requests.
        """
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
        """
        Return headers with the authorization token.

        :returns: The authorization headers as a dictionary.
        :rtype: dict
        """
        if not self.access_token:
            raise Exception("Authentication token is missing")
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _send_http_request(self, url: str, method: str, json: Optional[Dict] = None, data: Optional[Dict] = None,
                           params: Optional[Dict] = None, headers: Optional[Dict] = None) -> requests.Response:
        """
        Send HTTP request to the Playtomic server.

        :param str url: The URL for the HTTP request.
        :param str method: The HTTP request method (GET, POST, etc.).
        :param dict json: (optional) The JSON payload for the request.
        :param dict data: (optional) The form data for the request.
        :param dict params: (optional) The query parameters for the request.
        :param dict headers: (optional) The HTTP headers for the request.

        :returns: The instance of :class:`Response <requests.Response>`.
        :rtype: requests.Response
        """
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
        """
        Send HTTP request to Playtomic server, with automatic token refresh if needed.

        :param str method: The HTTP request method (GET, POST, etc.).
        :param str endpoint: The API endpoint to call.
        :param dict payload: (optional) The JSON payload for the request.

        :returns: The JSON response from the API.
        :rtype: dict
        """
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
        """
        Refresh the authentication token if expired.

        :raises: :class:`requests.HTTPError` if the refresh fails.
        """
        logger.debug("Refreshing access token.")
        refresh_url = f"{self.BASE_URL}/v3/auth/refresh"
        payload = {"refresh_token": self.refresh_token}
        headers = {"Content-Type": "application/json"}

        response = self._send_http_request(url=refresh_url, method="POST", json=payload, headers=headers)
        data = response.json()
        self.access_token = data.get("access_token")
        self.refresh_token = data.get("refresh_token")
        logger.info("Access token refreshed successfully.")

