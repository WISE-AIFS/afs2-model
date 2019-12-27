import json
import logging
import os
from io import BytesIO
import afs.utils as utils
import re
import base64
from uuid import uuid4
from afs.utils import upload_file_to_blob
from afs.get_env import AfsEnv


class models(AfsEnv):
    def __init__(
        self, target_endpoint=None, instance_id=None, auth_code=None, token=None
    ):
        """Connect to afs models service, user can connect to service by enviroment parameter. Another way is input when created.
        """
        super(models, self).__init__(target_endpoint, instance_id, auth_code, token)
        self.entity_uri = "model_repositories"
        self.sub_entity_uri = "models"
        self.metafile_uri = "model_metafiles"
        self.repo_id = None
        self.model_id = None

        # Blob info
        self._blob_endpoint = self.blob_endpoint
        self._blob_accessKey = self.blob_accessKey
        self._blob_secretKey = self.blob_secretKey

    def set_blob_credential(
        self, blob_endpoint, encode_blob_accessKey, encode_blob_secretKey
    ):
        """Set blob credential when upload the big model.

        :param str blob_endpoint: blob endpoint
        :param str encode_blob_accessKey: blob accessKey encode with base64
        :param str encode_blob_secretKey: blob secretKey encode with base64
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
            resp = self._get(extra_paths=extra_paths, params=params).json()
        else:
            extra_paths = [self.repo_id, self.sub_entity_uri]
            resp = self._get(extra_paths=extra_paths).json()

        if resp["resources"]:
            model_id = resp["resources"][0]["uuid"]
        else:
            return None
        return model_id

    def download_model(
        self, save_path, model_repository_name=None, model_name=None, last_one=False
    ):
        """Download model from model repository to a file.

        :param str model_repository_name: The model name exists in the model repository
        :param str save_path: The path exist in the file system
        :param str model_name: Get the specific model file from the model reposiotry
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
        if model_id:
            extra_paths = [self.repo_id, self.sub_entity_uri, model_id]
            params = {"alt": "media"}
            resp = self._get(params=params, extra_paths=extra_paths)
        else:
            raise ValueError("Model with name {} not found.".format(model_name))

        try:
            with open(save_path, "wb") as f:
                f.write(resp.content)
        except Exception as e:
            raise RuntimeError("Write download file error. Exception: {}".format(e))

        return True

    def upload_model(
        self,
        model_path,
        accuracy=None,
        loss=None,
        tags={},
        extra_evaluation={},
        model_repository_name=None,
        model_name=None,
        blob_mode=False,
    ):
        """Upload model to model repository. (Support v2 API)

        :param str model_path:  (required) model filepath 
        :param float accuracy: (optional) model accuracy value, between 0-1
        :param float loss: (optional) model loss value
        :param dict tags: (optional) tag from model
        :param dict extra_evaluation: (optional) other evaluation from model
        :param str model_name: (optional) Give model a name or a default name 
        :param str model_repository_name: (optional) model_repository_name
        :param bool blob_mode: (optional) upload model direct to blob mode, default False
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
            raise TypeError("Type error, model_name  cannot convert to string")

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
                pai_data_dir = json.loads(pai_data_dir)
                if "data" in pai_data_dir and "type" in pai_data_dir:
                    data = pai_data_dir["data"]
                    firehose_type = pai_data_dir["type"]

                    if "machineIdList" in data and firehose_type == "apm-firehose":
                        machineIdList = data.get("machineIdList", [None]).pop(0)

                        if machineIdList:
                            tags.update({"apm_node": str(machineIdList)})
            except Exception as e:
                print(
                    "PAI_DATA_DIR value is not valid json format for apm_node. Exception:{}, Value: {}".format(e, pai_data_dir)
                )

        # Evaluation result
        evaluation_result.update(extra_evaluation)
        data = dict(
            tags=json.dumps(tags), evaluation_result=json.dumps(evaluation_result)
        )
        # model name
        if model_name:
            self._naming_rule(model_name)
            data.update({"name": model_name})

        extra_paths = [self.repo_id, self.sub_entity_uri]
        # Load model size < 300 MB
        file_size = os.path.getsize(model_path)
        if file_size < (300 * 1024 * 1024) and not blob_mode:
            with open(model_path, "rb") as f:
                model_file = BytesIO(f.read())
            model_file.seek(0)
            files = {"model": model_file}

            resp = self._create(
                data=data, files=files, extra_paths=extra_paths, form="data"
            )

        # Between 300M - 1G model file
        elif file_size < (1024 * 1024 * 1024) or blob_mode:
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
            self.model_id = resp.json()["uuid"]
            key = "models/{}/{}/{}".format(self.instance_id, self.repo_id, self.model_id)

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
                extra_paths = [self.repo_id, self.sub_entity_uri, self.model_id]
                resp = self._del(extra_paths=extra_paths)
                raise ex

            # Update PUT Model File_info
            extra_paths = [
                self.repo_id,
                self.sub_entity_uri,
                self.model_id,
                "file_info",
            ]
            put_payload = {"size": object_size}
            resp = self._put(extra_paths=extra_paths, data=put_payload)

        else:
            raise Exception("The size of the file has exceeded the upper limit of 1G")

        if int(resp.status_code / 100) == 2:
            resp = resp.json()
            self.model_id = resp.get("uuid")
            return resp
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

    def upload_model_metafile(self, file_path, name, model_repository_name=None):
        """Upload model metafile
        :param file_path: model name.
        :param name: model metafile name.
        :param model_repository_name: model repository name.
        :return: dict API
        """

        if model_repository_name:
            self.get_model_repo_id(model_repository_name)

        if not (
            self._blob_endpoint
            and self._blob_accessKey
            and self._blob_secretKey
            and self.bucket_name
        ):
            raise ValueError(
                "Blob information is not enough to put object to blob, {}, {}, {}, {}".foramt(self._blob_endpoint, self._blob_accessKey, self._blob_secretKey, self.bucket_name)
            )

        # Create model metadata
        if name:
            self._naming_rule(name)
            payload = {"name": name}
        else:
            raise ValueError("Name of model metafile is empty.")
        extra_paths = [self.repo_id, self.metafile_uri]

        resp = self._create(data=payload, extra_paths=extra_paths, form="json")
        self.model_metadata_id = resp.json()["uuid"]

        key = resp.json()["blob_key"]

        try:
            object_size = upload_file_to_blob(
                self._blob_endpoint,
                self._blob_accessKey,
                self._blob_secretKey,
                self.bucket_name,
                key,
                file_path,
            )
        except ConnectionError as ex:
            # Delete model metadata if connection error
            extra_paths = [self.repo_id, self.metafile_uri, self.model_metadata_id]
            resp = self._del(extra_paths=extra_paths)
            raise ex

        # Update PUT Model metafile File_info
        extra_paths = [
            self.repo_id,
            self.metafile_uri,
            self.model_metadata_id,
            "file_info",
        ]
        put_payload = {"size": object_size}
        resp = self._put(extra_paths=extra_paths, data=put_payload)

        if int(resp.status_code / 100) == 2:
            resp = resp.json()
            self.model_metadata_id = resp.get("uuid")
            return resp
        else:
            return resp.text

    def get_model_metafile_id(self, name, model_repository_name=None):
        """Get model metafile id by name.
        
        :param str name: model metafile name..
        :param str model_repository_name: model respository name where the model metafile is.
        :return: str model metafile id
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

        if name:
            params = dict(name=name)
            extra_paths = [self.repo_id, self.metafile_uri]
            resp = self._get(extra_paths=extra_paths, params=params).json()

        if resp["resources"]:
            model_metafile_id = resp["resources"][0]["uuid"]
        else:
            return None
        return model_metafile_id

    def delete_model_metafile(self, name, model_repository_name=None):
        """Delete model metafile.
        
        :param model_name: model metafile name.
        :param model_repository_name: model repository name.
        :return: bool
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
        model_metafile_id = self.get_model_metafile_id(name=name)
        extra_paths = [self.repo_id, self.metafile_uri, model_metafile_id]
        resp = self._del(extra_paths=extra_paths)

        if int(resp.status_code / 100) == 2:
            return True
        else:
            return False

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
        if len(name) > 42 or len(name) < 1:
            raise ValueError("Name length is upper limit 1-42 char")

        pattern = re.compile(r"(?!.*[^a-zA-Z0-9-_.]).{1,42}")
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
