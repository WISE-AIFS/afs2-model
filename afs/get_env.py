import os, json
import requests
import warnings
import afs.utils as utils
import afs


class AfsEnv:
    def __init__(
        self, target_endpoint=None, instance_id=None, auth_code=None, token=None
    ):
        self.version = os.getenv("AFS_API_VERSION", os.getenv("version", ""))
        if target_endpoint == None or instance_id == None:
            self.afs_url = self.target_endpoint = os.getenv("afs_url", None)
            self.instance_id = os.getenv("instance_id", None)

            if self.target_endpoint == None or self.instance_id == None:
                raise ValueError(
                    "Environment parameters need afs_url={0}, instance_id={1}".format(
                        self.target_endpoint, self.instance_id
                    )
                )
        else:
            self.afs_url = self.target_endpoint = target_endpoint
            self.instance_id = instance_id

        self.session = requests.Session()
        self.token = None

        if auth_code == None:
            self.auth_code = os.getenv("auth_code", None)
        else:
            self.auth_code = auth_code

        self.token = token
        if self.auth_code != None:
            self.session.headers.update({"Authorization": "Bearer {token}"})
        else:
            raise ValueError("There is no auth_code and token to verify.")

        if not self.target_endpoint.endswith("/"):
            self.target_endpoint = self.target_endpoint + "/"

        self.api_version, self.afs_portal_version = self._get_api_version()
        self.target_endpoint = self.target_endpoint + self.api_version + "/"
        self.bucket_name = self._get_blob_bucket()

    def _get_api_version(self):
        url = utils.urljoin(self.target_endpoint, extra_paths={})
        response = utils._check_response(self.session.get(url, verify=False))

        afs_portal_version = response.json().get("AFS_version", None)
        if afs_portal_version != afs.__version__:
            warnings.warn(
                "SDK version: {0}, and AFS api version: {1}. It might cause some compatibility issues. Readthedocs: https://afs-sdk.readthedocs.io/en/latest/Examples.html#models".format(
                    afs.__version__, afs_portal_version
                )
            )

        if response.json().get("AFS_version", None):
            return response.json()["API_version"], afs_portal_version
        else:
            raise ConnectionError("Cannot fetch AFS server from {}".format(url))

    def _get_blob_bucket(self):
        url = utils.urljoin(self.afs_url, "info", "bucket", extra_paths=[])
        response = self.session.get(
            url, params={"auth_code": self.auth_code}, verify=False
        )
        if response.status_code == 200:
            bucket = response.json()["bucket"]
            return bucket
        else:
            print(f"Not found {url}, {response.text}")
            return None
