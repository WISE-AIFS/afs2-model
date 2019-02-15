from urllib.parse import urljoin

from .base import APISession
from .exceptions import SSOException


class SSOClient:
    def __init__(self, api_endpoint, api_version: str = 'v2', session=None):
        self.api_endpoint = api_endpoint
        self.api_version = api_version
        self._session = APISession(session=session)

    def get_sso_token(self, username: str, password: str):
        path = '{}/auth/native'.format(self.api_version)
        url = urljoin(self.api_endpoint, path)

        resp = self._session.post(
            url,
            json={'username': username, 'password': password}
        )

        token = resp.get('accessToken')
        if not token:
            raise SSOException('No accessToken in response')

        return token

    def refresh_sso_token(self, token):
        pass
