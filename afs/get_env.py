import os, json
import requests
import warnings
import afs.utils as utils
import afs
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry

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

        self.blob_id = None
        self.blob_endpoint =  None
        self.blob_accessKey = None
        self.blob_secretKey = None
        self.blob_record_id = None
        self.bucket_name = None
        self._get_blobstore_credential()

        print('Using AFS version {}'.format(self.afs_version))


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


    def _get_blobstore_credential(self):
        blobstore = os.getenv("blobstore", None)
        blob_id = os.getenv('blob_id')
        blob_record_id = os.getenv('blob_record_id')
        
        if blob_id and blob_record_id:
            self.blob_id = blob_id
            self.blob_record_id = blob_record_id
        elif blobstore:
            try:
                blobstore = json.loads(blobstore)
                if not blobstore.get('credentials'):
                    self.blob_id = blobstore.get('blob_id')
                    self.blob_record_id = blobstore.get('blob_record_id')
            except Exception as e:
                raise EnvironmentError('The env blobstore format is error.\n \
                    Please set blob credentials manually.\n \
                    Reference models.set_blob_credential usage. \n \
                    Exception: {}'.format(e))
        else:
            raise EnvironmentError('Please set blob credentials manually.\n \
                Reference models.set_blob_credential usage.')
        
        self.openpai_id = os.getenv('openpai_id')
        pai_job_name = os.getenv('PAI_JOB_NAME')
        url = utils.urljoin(
            self.target_endpoint, "instances", self.instance_id, "blobs", self.blob_id, "info", extra_paths=[])
        params = {
            'openpai_id': self.openpai_id, 
            'pai_job_name': pai_job_name,
        }
        if not self.token:
            params.update({"auth_code": self.auth_code})

        retries = Retry(
            total=5, 
            method_whitelist=frozenset(['GET', 'POST']), 
            status_forcelist=[404, 500, 502, 503, 504]
            )
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

        response = self.session.get(
            url, params=params, verify=False
        )
        if response.status_code / 100 == 2:
            blobstore = response.json()
            self.blob_record_id = blobstore.get('blob_record_id')
            self.bucket_name = blobstore.get('bucket_name')
            self.blob_endpoint = blobstore.get('endpoint')
            self.blob_accessKey = blobstore.get('access_key')
            self.blob_secretKey = blobstore.get('secret_key')
        else:
            raise ConnectionError("Not found {}, {}".format(url, response.text))
