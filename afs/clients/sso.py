from urllib.parse import urljoin

from jwt import decode as jwt_decode

from .base import APISession
from .exceptions import SSOClientError


class SSOClient:
    """
    Client class for EI-PaaS SSO.

    :param str api_endpoint: The api endpoint of EI-PaaS SSO.
    :param str api_version: The SSO API version. Default is **v2.0**.
    :param Session session: The session object of this client.
    :raises SSOClientError:
    """

    def __init__(self, api_endpoint, api_version: str = "v2.0", session=None):
        self.api_endpoint = api_endpoint
        self.api_version = api_version
        if not session:
            session = APISession()
        self._session = session

    def get_sso_token(self, username: str, password: str):
        path = "{}/auth/native".format(self.api_version)
        url = urljoin(self.api_endpoint, path)

        resp = self._session.post(
            url, json={"username": username, "password": password}
        )

        token = resp.get("accessToken")
        if not token:
            raise SSOClientError("No accessToken in response")

        return token

    def get_refresh_token(self, token):
        decoded_token = jwt_decode(token, verify=False)
        refresh_token = decoded_token.get("refreshToken")
        if not refresh_token:
            raise SSOClientError("No refreshToken in response")
        return refresh_token

    def refresh_sso_token(self, token):
        path = "{}/token".format(self.api_version)
        url = urljoin(self.api_endpoint, path)

        refresh_token = self.get_refresh_token(token)
        resp = self._session.post(url, json={"token": refresh_token})

        token = resp.get("accessToken")
        if not token:
            raise SSOClientError("No accessToken in response")

        return token
