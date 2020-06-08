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
        self.token = token
        self.auth_code = auth_code

        if self.token:
            self.session.headers.update({"Authorization": token})
        elif auth_code == None:
            self.auth_code = os.getenv("auth_code", None)

        if self.auth_code == None and self.token == None:
            raise ValueError("There is no auth_code and token to verify.")

        if not self.target_endpoint.endswith("/"):
            self.target_endpoint = self.target_endpoint + "/"

        self.api_version, self.afs_version = self._get_api_version()
        self.target_endpoint = self.target_endpoint + self.api_version + "/"

        self.blob_endpoint =  None
        self.blob_accessKey = None
        self.blob_secretKey = None
        self.blob_record_id = None
        self.bucket_name = None
        self._get_blobstore_credential()
        # self.blob_record_id = utils.hash_blob_md5(self.instance_id, self.blob_accessKey)


    def _get_api_version(self):
        # Fetch api-afs root info 
        url = utils.urljoin(self.target_endpoint, extra_paths={})
        response = utils._check_response(self.session.get(url, verify=False))

        # Check AFS version
        afs_version = response.json().get("AFS_version", None)

        # Check API version
        api_version = response.json().get("API_version", None)
        if not api_version:
            raise ValueError("No API_version from api-afs.")

        if response.json().get("AFS_version", None):
            return api_version, afs_version
        else:
            raise ConnectionError("Cannot fetch AFS server from {}.".format(url))

    def _get_blob_bucket(self):
        url = utils.urljoin(self.afs_url, "info", "bucket", extra_paths=[])
        response = self.session.get(
            url, params={"auth_code": self.auth_code}, verify=False
        )
        if response.status_code == 200:
            bucket = response.json()["bucket"]
            return bucket
        else:
            print("Not found {}, {}".format(url, response.text))
            return None

    def _get_blobstore_credential(self):
        blobstore = os.getenv("blobstore", None)
        if blobstore:
            try:
                blobstore = json.loads(blobstore)
                self.blob_record_id = blobstore.get('blob_record_id')
                self.bucket_name = blobstore.get('bucket_name')
                credentials = blobstore.get('credentials')
                self.blob_endpoint = credentials.get('endpoint')
                self.blob_accessKey = credentials.get('accessKey')
                self.blob_secretKey = credentials.get('secretKey')
            except Exception as e:
                print('The env blobstore format is error.\n \
                    Please set blob credentials manually.\n \
                    Reference models.set_blob_credential usage.')
        else:
            print('Please set blob credentials manually.\n \
                Reference models.set_blob_credential usage.')

    def check_blob_connection(self):
        if self.blob_endpoint and \
        self.blob_accessKey and \
        self.blob_secretKey and \
        self.blob_record_id and \
        self.bucket_name:
            return True
        else:
            raise ValueError("No values in blob_endpoint, blob_accessKey, blob_secretKey, blob_record_id, bucket_name. \
                {}, {}, {}, {}, {}".format(self.blob_endpoint, self.blob_accessKey, self.blob_secretKey, self.blob_record_id, self.bucket_name))
