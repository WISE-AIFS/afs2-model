import json
import logging
import os
from io import BytesIO
import afs.utils as utils
import re
import base64
from uuid import uuid4
from afs.utils import (upload_file_to_blob, dowload_file_from_blob,
                        encrypt, decrypt)
from afs.get_env import AfsEnv

UPLOAD_LIMIT_SIZE_GB = 5

class models(AfsEnv):
    def __init__(
        self, target_endpoint=None, instance_id=None, auth_code=None, token=None
    ):
        """Connect to afs models service, user can connect to service by enviroment parameter. Another way is input when created.
        """
        super(models, self).__init__(target_endpoint, instance_id, auth_code, token)
        self.entity_uri = "model_repositories"
        self.sub_entity_uri = "models"
        self.repo_id = None

        # Blob info
        self._blob_endpoint = self.blob_endpoint
        self._blob_accessKey = self.blob_accessKey
        self._blob_secretKey = self.blob_secretKey

    def set_blob_credential(
        self, blob_endpoint, encode_blob_accessKey, encode_blob_secretKey, blob_record_id, bucket_name
    ):
        """Set blob credential when upload the big model.

        :param str blob_endpoint: blob endpoint
        :param str encode_blob_accessKey: blob accessKey encode with base64
        :param str encode_blob_secretKey: blob secretKey encode with base64
        :param str blob_record_id: MD5 with instance_id + '_' + accessKey
        :param str bucket_name: blob bucket name
        """
        try:
            _blob_accessKey = str(base64.b64decode(encode_blob_accessKey), "utf-8")
            _blob_secretKey = str(base64.b64decode(encode_blob_secretKey), "utf-8")
        except Exception as e:
            raise ValueError(
                "encode_blob_accessKey, encode_blob_secretKey cannot be decoded."
            )

        self._blob_endpoint = blob_endpoint
        self._blob_accessKey = _blob_accessKey
        self._blob_secretKey = _blob_secretKey
        self.blob_record_id = blob_record_id
        self.bucket_name = bucket_name
        
    def get_model_repo_id(self, model_repository_name=None):
        """Get model repository by name.
        
        :param str model_repository_name:  
        :return: str model repository id
        """
        if model_repository_name:
            params = dict(name=model_repository_name)
            resp = self._get(params=params).json()

            if resp["resources"]:
                repo_id = resp["resources"][0]["uuid"]
            else:
                self.repo_id = None
                return None
            self.repo_id = repo_id

        return self.repo_id

    def get_model_id(self, model_name=None, model_repository_name=None, last_one=True):
        """Get model id by model name.
        
        :param str model_name: model name. No need if last_one is true.
        :param str model_repository_name: model respository name where the model is.
        :param bool last_one: auto get the model_repository last one model
        :return: str model id
        """
        if not model_repository_name:
            if not self.repo_id:
                raise ValueError("Please enter model_repository_name.")
        else:
            self.get_model_repo_id(model_repository_name=model_repository_name)
            if not self.repo_id:
                raise ValueError(
                    "Model repository with name {} not found.".format(
                        model_repository_name
                    )
                )

        if model_name:
            params = dict(name=model_name)
            extra_paths = [self.repo_id, self.sub_entity_uri]
            resp = self._get(extra_paths=extra_paths, params=params)
            resp = resp.json()
            for resource in resp["resources"]:
                if resource['name'] == model_name:
                    return resource['uuid']
        else:
            extra_paths = [self.repo_id, self.sub_entity_uri]
            resp = self._get(extra_paths=extra_paths)
            resp = resp.json()
            resources = resp["resources"]
            if resources:
                return resources[0]["uuid"]
        return None

    def download_model(
        self, save_path, model_repository_name=None, model_name=None, last_one=False
    ):
        """Download model from model repository to a file.

        :param str model_repository_name: The model name exists in the model repository
        :param str save_path: The path exist in the file system
        :param str model_name: Get the specific model file from the model reposiotry, if getting last one value for None.
        :param str last_one: Get the last uploading model from the model repository.
        """
        if model_repository_name:
            self.get_model_repo_id(model_repository_name)

        if not self.repo_id:
            raise ValueError("There is no specific repo_id to download.")

        model_id = self.get_model_id(
            model_name=model_name,
            model_repository_name=model_repository_name,
            last_one=last_one,
        )

        key = "models/{}/{}/{}".format(self.instance_id, self.repo_id, model_id)
        dowload_file_from_blob(
            self._blob_endpoint,
            self._blob_accessKey,
            self._blob_secretKey,
            self.bucket_name,
            key,
            save_path,
        )
        return True

    def upload_model(
        self,
        model_path,
        accuracy=None,
        loss=None,
        tags={},
        extra_evaluation={},
        feature_importance=None,
        coefficient=None,
        model_repository_name=None,
        model_name=None,
        encrypt_key=''
    ):
        """Upload model to model repository. (Support v2 API)

        :param str model_path:  (required) model filepath 
        :param float accuracy: (optional) model accuracy value, between 0-1
        :param float loss: (optional) model loss value
        :param dict tags: (optional) tag from model
        :param dict extra_evaluation: (optional) other evaluation from model
        :param str model_name: (optional) Give model a name or a default name 
        :param str model_repository_name: (optional) model_repository_name
        :param list feature_importance: (optional) feature_importance is the record how the features important in the model
        :param list coefficient: (optional) coefficient indicates the direction of the relationship between a predictor variable and the response 
        :param str encrypt_key: (optional) If there is a encrypt_key, use the encrypt_key to encrypt the model
        :return: dict. the information of the upload model.
        """

        if not isinstance(tags, dict) or not isinstance(extra_evaluation, dict):
            raise ValueError(
                "Type error, accuracy and loss are float, and tags and extra_evaluation are dict."
            )

        # Evaluation_result info
        evaluation_result = {}
        if accuracy is not None:
            if not isinstance(accuracy, (float, int)):
                raise TypeError("Type error, accuracy is float.")
            if accuracy > 1.0 or accuracy < 0:
                raise ValueError("Accuracy value should be between 0-1")
            evaluation_result.update({"accuracy": accuracy})

        if loss is not None:
            if not isinstance(loss, (float, int)):
                raise TypeError("Type error, loss is float.")
            evaluation_result.update({"loss": loss})

        if not isinstance(model_path, str):
            raise TypeError("Type error, model_name cannot convert to string")

        if not os.path.isfile(model_path):
            raise IOError("File not found, model path is not exist.")

        # Check default repo_id
        if not self.repo_id:
            # Find model_repo_id from name
            if model_repository_name:
                self.get_model_repo_id(model_repository_name)
                # If not found, create one
                if not self.repo_id:
                    self.repo_id = self.create_model_repo(model_repository_name)
            else:
                raise ValueError("Please enter model_repository_name")

        # Fetch tags apm_node
        pai_data_dir = os.getenv("PAI_DATA_DIR", None)
        if pai_data_dir:
            try:
                pai_data_dir = str(base64.b64decode(pai_data_dir), "utf-8")
                # double load to escape double quotes
                firehose = json.loads(pai_data_dir)
                if ("data" in firehose) and ("type" in firehose):
                    data = firehose["data"]
                    firehose_type = firehose["type"]

                    if "machineIdList" in data and firehose_type == "apm-firehose":
                        machineIdList = data.get("machineIdList", [None]).pop(0)
                        if machineIdList:
                            tags.update({"apm_node": str(machineIdList)})
            except Exception as e:
                print(
                    "PAI_DATA_DIR value is not valid json format for apm_node. Exception: {}, Value: {}".format(e, pai_data_dir)
                )

        # record encrypy or not
        tags.update({"is_encrypted": bool(encrypt_key)})

        if encrypt_key:
            data = None
            with open(model_path, 'rb') as f:
                data = f.read()
                data = encrypt(data, encrypt_key)
            with open(model_path, 'wb') as f:
                f.write(data)

        # Evaluation result
        evaluation_result.update(extra_evaluation)
        data = dict(
            tags=json.dumps(tags), 
            evaluation_result=json.dumps(evaluation_result),
        )
        if feature_importance:
            data.update({'feature_importance': json.dumps(feature_importance)})
        if coefficient:
            data.update({'coefficient': json.dumps(coefficient)})

        if self.afs_version >= '3.1.3':
            data.update(
                {
                    'dataset_id': os.getenv('dataset_id'),
                    'afs_target': os.getenv('afs_target'),
                }
            )

        # model name
        if model_name:
            self._naming_rule(model_name)
            data.update({"name": model_name})

        extra_paths = [self.repo_id, self.sub_entity_uri]
        file_size = os.path.getsize(model_path)
        # upload model file
        if file_size < (UPLOAD_LIMIT_SIZE_GB*2**30):
            if not (
                self._blob_endpoint
                and self._blob_accessKey
                and self._blob_secretKey
                and self.bucket_name
            ):
                raise ValueError(
                    "Blob information is not enough to put object to blob, {}, {}, {}, {}".format(self._blob_endpoint, self._blob_accessKey, self._blob_secretKey, self.bucket_name)
                )

            # Create model metadata
            resp = self._create(data=data, extra_paths=extra_paths, form="data")
            model_id = resp.json()["uuid"]
            key = "models/{}/{}/{}".format(self.instance_id, self.repo_id, model_id)

            try:
                object_size = upload_file_to_blob(
                    self._blob_endpoint,
                    self._blob_accessKey,
                    self._blob_secretKey,
                    self.bucket_name,
                    key,
                    model_path,
                )
            except ConnectionError as ex:
                # Delete model metadata if connection error
                extra_paths = [self.repo_id, self.sub_entity_uri, model_id]
                resp = self._del(extra_paths=extra_paths)
                raise ex

            # Update PUT Model File_info
            extra_paths = [
                self.repo_id,
                self.sub_entity_uri,
                model_id,
                "file_info",
            ]
            put_payload = {"size": object_size, "blob_record_id": self.blob_record_id}
            resp = self._put(extra_paths=extra_paths, data=put_payload)
        else:
            raise Exception("The size of the file has exceeded the upper limit of {}G".format(UPLOAD_LIMIT_SIZE_GB))

        if int(resp.status_code / 100) == 2:
            return resp.json()
        else:
            raise RuntimeError(resp.text)

    def create_model_repo(self, model_repository_name):
        """
        Create a new model repository. (Support v2 API)
        
        :param str model_repository_name: (optional)The name of model repository.
        :return: the new uuid of the repository
        """
        if isinstance(model_repository_name, str):
            self._naming_rule(model_repository_name)
        else:
            raise TypeError("Repo name must be string")

        payload = dict(name=model_repository_name)
        resp = self._create(payload)
        self.repo_id = resp.json()["uuid"]
        return self.repo_id

    def get_latest_model_info(self, model_repository_name=None):
        """
        Get the latest model info, including created_at, tags, evaluation_result. (Support v2 API)
        
        :param model_repository_name: (optional)The name of model repository.
        :return: dict. the latest of model info in model repository.
        """
        model_id = self.get_model_id(
            model_repository_name=model_repository_name, last_one=True
        )

        if model_id:
            extra_paths = [self.repo_id, self.sub_entity_uri, model_id]
            resp = self._get(extra_paths=extra_paths)
            return resp.json()
        else:
            raise ValueError("Model not found.")

    def get_model_info(self, model_name, model_repository_name=None):
        """Get model info, including created_at, tags, evaluation_result. (V2 API)
        
        :param model_name: model name
        :param model_repository_name: The name of model repository.
        :return: dict model info
        """
        if not self.get_model_repo_id(model_repository_name=model_repository_name):
            raise ValueError("Model_repository not found.")

        model_id = self.get_model_id(
            model_name=model_name, model_repository_name=model_repository_name
        )

        if model_id:
            extra_paths = [self.repo_id, self.sub_entity_uri, model_id]
            resp = self._get(extra_paths=extra_paths)
        else:
            raise ValueError("Model not found.")

        return resp.json()

    def delete_model_repository(self, model_repository_name):
        """Delete model repository.
        
        :param model_repository_name: model repository name.
        :return: bool 
        """
        if not self.get_model_repo_id(model_repository_name):
            raise ValueError("Model_repository not found.")

        extra_paths = [self.repo_id]
        resp = self._del(extra_paths=extra_paths)

        if int(resp.status_code / 100) == 2:
            return True
        else:
            return False

    def delete_model(self, model_name, model_repository_name=None):
        """Delete model.
        
        :param model_name: model name.
        :param model_repository_name: model repository name.
        :return: bool
        """
        if not self.get_model_repo_id(model_repository_name=model_repository_name):
            raise ValueError("Model_repository not found.")

        model_id = self.get_model_id(
            model_name, model_repository_name=model_repository_name, last_one=False
        )
        if not model_id:
            raise ValueError("Model not found.")
        extra_paths = [self.repo_id, self.sub_entity_uri, model_id]
        resp = self._del(extra_paths=extra_paths)

        if int(resp.status_code / 100) == 2:
            return True
        else:
            return False

    def decrypt_model(self, model, decrypt_key):
        """Decrypt model.
        
        :param object model: the object of model
        :param str decrypt_key: use decrypt_key to decrypt the model
        :return: object
        """
        return decrypt(model, decrypt_key)

    def download_model_from_blob(
        self, instance_id, model_repository_id, model_id, save_path,
        blob_endpoint, blob_accessKey, blob_secretKey, bucket_name):
        """API dowload model
        : instance_id: AIFS instance id
        : model_repository_id: model repository id in instance 
        : model_id: model id in model repository 
        : save_path: download filepath
        : blob_endpoint: blob 
        : blob_accessKey: 
        : blob_secretKey:
        : bucket_name:
        """
        key = "models/{}/{}/{}".format(instance_id, model_repository_id, model_id)
        _blob_accessKey = str(base64.b64decode(blob_accessKey), "utf-8")
        _blob_secretKey = str(base64.b64decode(blob_secretKey), "utf-8")
        dowload_file_from_blob(
            blob_endpoint,
            _blob_accessKey,
            _blob_secretKey,
            bucket_name,
            key,
            save_path,
        )
        return True

    def _create(self, data, files=None, extra_paths=[], form="json"):
        url = utils.urljoin(
            self.target_endpoint,
            "instances",
            self.instance_id,
            self.entity_uri,
            extra_paths=extra_paths,
        )

        if not files:
            if form == "json":
                response = utils._check_response(
                    self.session.post(
                        url,
                        params=dict(auth_code=self.auth_code),
                        json=data,
                        verify=False,
                    )
                )
            elif form == "data":
                response = utils._check_response(
                    self.session.post(
                        url,
                        params=dict(auth_code=self.auth_code),
                        data=data,
                        verify=False,
                    )
                )
        else:
            if form == "json":
                response = utils._check_response(
                    self.session.post(
                        url,
                        params=dict(auth_code=self.auth_code),
                        json=data,
                        files=files,
                        verify=False,
                    )
                )
            elif form == "data":
                response = utils._check_response(
                    self.session.post(
                        url,
                        params=dict(auth_code=self.auth_code),
                        data=data,
                        files=files,
                        verify=False,
                    )
                )

        return response

    def _get(self, params={}, extra_paths=[]):
        url = utils.urljoin(
            self.target_endpoint,
            "instances",
            self.instance_id,
            self.entity_uri,
            extra_paths=extra_paths,
        )

        get_params = {}
        get_params.update(dict(auth_code=self.auth_code))
        get_params.update(params)
        response = utils._check_response(
            self.session.get(url, params=get_params, verify=False)
        )
        return response

    def _del(self, params={}, extra_paths=[]):
        url = utils.urljoin(
            self.target_endpoint,
            "instances",
            self.instance_id,
            self.entity_uri,
            extra_paths=extra_paths,
        )

        get_params = {}
        get_params.update(dict(auth_code=self.auth_code))
        get_params.update(params)
        response = utils._check_response(
            self.session.delete(url, params=get_params, verify=False)
        )
        return response

    def _naming_rule(self, name):
        limit = 72
        if len(name) > limit or len(name) < 1:
            raise ValueError("Name length is upper limit 1-{} char".format((limit)))

        pattern = re.compile(r"(?!.*[^a-zA-Z0-9-_.]).{1,72}")
        match = pattern.match(name)
        if match is None:
            raise ValueError("Naming rule is only a-z, A-Z, 0-9, - and _ allowed.")

        return True

    def _put(self, data, extra_paths=[]):
        url = utils.urljoin(
            self.target_endpoint,
            "instances",
            self.instance_id,
            self.entity_uri,
            extra_paths=extra_paths,
        )
        get_params = {}
        get_params.update(dict(auth_code=self.auth_code))
        response = utils._check_response(
            self.session.put(url, params=get_params, json=data, verify=False)
        )
        return response
