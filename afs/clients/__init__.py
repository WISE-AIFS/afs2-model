from .base import APISession
from .exceptions import AFSClientError
from .instances import InstancesClient
from .sso import SSOClient


class AFSClient:
    """
    Client class for AFS.

    :param str api_endpoint: The api endpoint of AFS server.
    :param str api_version: The version of AFS API.
    :param str sso_api_version: The SSO API version. Default is **v2.0**.
    :param str token: The SSO token used to access resources on EI-PaaS platform.
    :param str username: The SSO username used to sign in to EI-PaaS platform.
    :param str password: The SSO password used to sign in to EI-PaaS platform.
    :param bool ssl: Set to False can ignore SSL verify. Default is **True**.
    :raises AFSClientError: If get api version from AFS server failed or no available token.
    """

    def __init__(
        self,
        api_endpoint,
        api_version: str = None,
        sso_api_version: str = "v2.0",
        token: str = None,
        username: str = None,
        password: str = None,
        ssl=True,
    ):

        self._session = APISession(ssl=ssl)

        # TODO: URL check
        self.api_endpoint = api_endpoint
        self.api_version = api_version or self.get_api_version()

        # Setup SSO client and token
        sso_endpoint = self.api_endpoint.replace("api-afs", "portal-sso")
        self.sso = SSOClient(
            api_endpoint=sso_endpoint,
            api_version=sso_api_version,
            session=self._session,
        )

        if token:
            pass

        elif username and password:
            token = self.sso.get_sso_token(username=username, password=password)

        else:
            raise AFSClientError("No available token or user for SSO")

        self._session.headers.update({"Authorization": "Bearer {}".format(token)})
        self._session.enable_auto_refresh_token(token, self.sso.refresh_sso_token)

        self.instances = InstancesClient(self)

    def get_api_info(self):
        """
        Get api information from AFS server.

        :return: The response from AFS server.
        :rtype: APIResponse
        :raises AFSClientError: Any error during request to or response from AFS Server.
        """
        try:
            resp = self._session.get(self.api_endpoint)
        except Exception as e:
            raise AFSClientError(e)
        return resp

    def get_api_version(self):
        """
        Get current API version from AFS server.

        :return: The AFS API version.
        :rtype: str
        :raises AFSClientError: Can not get API_version from AFS Server.
        """
        api_info = self.get_api_info()
        api_version = api_info.get("API_version")
        if not api_version:
            raise AFSClientError("No API_version in API info")

        return api_version
