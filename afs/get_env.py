import os, json
import requests
import warnings
import afs.utils as utils
import afs


class AfsEnv:
    def __init__(self, target_endpoint=None, instance_id=None, auth_code=None):
        self.version = os.getenv("AFS_API_VERSION", os.getenv("version", ""))

        if target_endpoint is None or instance_id is None or auth_code is None:
            self.afs_url = os.getenv("afs_url", None)
            self.target_endpoint = os.getenv("afs_url", None)
            self.auth_code = os.getenv("auth_code", None)
            self.instance_id = os.getenv("instance_id", None)

            if (
                self.target_endpoint == None
                or self.instance_id == None
                or self.auth_code == None
            ):
                raise AssertionError(
                    "Environment parameters need afs_url={0}, instance_id={1}, auth_code={2}".format(
                        self.target_endpoint, self.instance_id, self.auth_code
                    )
                )
        else:
            self.target_endpoint = target_endpoint
            self.auth_code = auth_code
            self.instance_id = instance_id

        if not self.target_endpoint.endswith("/"):
            self.target_endpoint = self.target_endpoint + "/"

        self.api_version, self.afs_portal_version = self._get_api_version()
        self.target_endpoint = self.target_endpoint + self.api_version + "/"
        self.bucket_name = self._get_blob_bucket()

    def _get_api_version(self):
        url = utils.urljoin(self.target_endpoint, extra_paths={})
        response = utils._check_response(requests.get(url, verify=False))

        afs_portal_version = response.json().get("AFS_version", None)
        if afs_portal_version != afs.__version__:
            warnings.warn(
                "SDK version is {0}, and AFS portal version is {1}. It will cause some compatibility issues. Readthedocs: https://afs-sdk.readthedocs.io/en/latest/Examples.html#models".format(
                    afs.__version__, afs_portal_version
                )
            )

        if response.json().get("AFS_version", None):
            return response.json()["API_version"], afs_portal_version
        else:
            raise ConnectionError("Cannot fetch AFS server from {}".format(url))

    def _get_blob_bucket(self):
        # url = utils.urljoin(self.afs_url, 'info', 'bucket', extra_paths=[])
        url = f"{self.afs_url}info/bucket"
        response = requests.get(url, params={"auth_code": self.auth_code}, verify=False)
        if response.status_code == 200:
            bucket = response.json()["bucket"]
            return bucket
        else:
            print(f"Not found {url}, {response.text}")
            return None
