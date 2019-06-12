import json
import os
import warnings
from functools import wraps
from io import BytesIO
from itertools import chain
from pathlib import Path
from tempfile import TemporaryFile
from urllib.parse import urljoin
from zipfile import ZIP_DEFLATED, ZipFile

import yaml
import requests


def state_serialization():
    def wrapper(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self._write_config()
            return result

        return wrapped

    return wrapper


class EIPaaSAFSSession:
    """
    Allow EI-PaaS user use AFS when develop analytic at local
    """

    def __init__(self, verify=True):
        self.verify = verify
        self.timeout = 15

        self.config_root = Path.home().joinpath(".eipass")
        self.config_path = self.config_root.joinpath("afs.json")

        if self.config_path.exists() and self.config_path.is_file():
            self._load_config()

    def _load_config(self):
        with open(self.config_path, "r") as f:
            config = f.read()

        if config:
            for key, value in json.loads(config).items():
                setattr(self, key, value)

    def _write_config(self):
        self.config_root.mkdir(exist_ok=True)
        with open(self.config_path, "w") as f:
            f.write(json.dumps(self._get_attributes(), indent=4))

    def _get_attributes(self):
        private_data = [
            "username",
            "password",
            # '_token'
        ]
        unserializable = ["session"]
        system_configs = ["config_root", "config_path"]
        exclude_keys = set(chain(private_data, unserializable, system_configs))
        attributes = {
            key: value
            for key, value in self.__dict__.items()
            if not callable(value) and key not in exclude_keys
        }
        return attributes

    @state_serialization()
    def login(self, target_endpoint, username, password):
        """
        Login to AFS

        :param str target_endpoint: The url for target AFS
        :param str username: The usename of your EI-PaaS SSO account
        :param str password: The password of your EI-PaaS SSO account
        """

        if not target_endpoint.startswith(("http://", "https://")):
            target_endpoint = "https://" + target_endpoint
        self.target_endpoint = target_endpoint

        resp = requests.get(urljoin(self.target_endpoint, "info"))

        if not resp.ok:
            message = {
                "error": "Get info from {0} failed".format(self.target_endpoint),
                "response": resp.text,
            }
            raise Exception(message)

        resp = resp.json()
        self.api_version = resp["API_version"]
        self.afs_version = resp["AFS_version"]

        resp = requests.post(
            self.target_endpoint,
            params={"login_type": "UAA"},
            data={"username": username, "password": password},
            timeout=self.timeout,
        )

        if not resp.ok:
            message = {
                "error": "Login to {0} as user {1} failed".format(
                    self.target_endpoint, username
                )
            }
            raise Exception(message)

        self._token = resp.json()["token"]

    def list_service_instances(self):
        """
        List service instances for user
        """
        if not getattr(self, "_token", None):
            message = {"error": "Please login first"}
            raise Exception(message)

        resp = requests.get(
            urljoin(
                self.target_endpoint, str(Path(self.api_version).joinpath("instances"))
            ),
            headers={"Authorization": "Bearer " + self._token},
            timeout=self.timeout,
        )

        if not resp.ok:
            message = {"error": "List service instances failed", "response": resp.text}
            raise Exception(message)

        return resp.json()

    @state_serialization()
    def target(self, service_instance_id=None):
        """
        If service_instance_id is None, this function will return current service instance id,
        Else will set service_instance_id as targeted service instance and get info of this service instance

        :param str service_instance_id: The service instance id for later usage
        """

        if not getattr(self, "_token", None):
            message = {"error": "Please login first"}
            raise Exception(message)

        if not service_instance_id:
            service_instance_id = getattr(self, "service_instance_id", None)
            if not service_instance_id:
                message = {"error": "Please login adn select service instance first"}
                raise Exception(message)

            target = {
                "service_instance_id": self.service_instance_id,
                "auth_code": self.auth_code,
            }

            return target

        resp = requests.get(
            urljoin(
                self.target_endpoint,
                str(Path(self.api_version).joinpath(service_instance_id)),
            ),
            headers={"Authorization": "Bearer " + self._token},
            timeout=self.timeout,
        )

        if not resp.ok:
            message = {
                "error": "Get info of service instance {0} failed".format(
                    service_instance_id
                ),
                "response": resp.text,
            }
            raise Exception(message)

        resp = resp.json()
        self.auth_code = resp.pop("auth_code")
        self.service_instance_id = resp.pop("instance_id")
        self.endpoints = resp

    @state_serialization()
    def push(self, source_path="./", manifest_path="./manifest.yml", name=None):
        """
        Push analytic app to workspace

        :param str source_path: The path of analytic app which you want to upload to your AFS instance
        :param str manifest_path: The path of manifest of your analytic app
        """
        workspace_endpoint = getattr(self, "endpoints", {}).get("workspace_endpoint")
        auth_code = getattr(self, "auth_code", None)
        if not workspace_endpoint or not auth_code:
            message = {"error": "Please login and select your AFS instance first"}
            raise Exception(message)

        source_path = Path(source_path).absolute()
        if not source_path.is_dir():
            message = {
                "error": "Source path {0} is not a directory".format(source_path)
            }
            raise Exception(message)

        manifest_path = Path(manifest_path).absolute()
        if not manifest_path.is_file() and manifest_path != source_path.joinpath(
            "manifest.yml"
        ):
            message = {
                "warning": "Manifest path {0} is not a file, use {1} as manifest".format(
                    manifest_path, source_path.joinpath("manifest.yml")
                )
            }
            warnings.warn(message)
            manifest_path = source_path.joinpath("manifest.yml")

        if not manifest_path.is_file():
            message = {"error": "Manifest path {0} is not file"}
            raise Exception(message)

        try:
            with open(manifest_path, "r") as f:
                manifest = yaml.load(f.read())

        except Exception:
            message = {"error": "Manifest is not valid yaml file"}
            raise Exception(message)

        if not name:
            try:
                name = manifest.get("applications")[0].get("name")

            except Exception:
                message = {"error": "Manifest seems not a valid cloud foundry manifest"}
                raise Exception(message)

        if not name:
            message = {"error": "Please provide name of your analytic app"}
            raise Exception(message)

        name += "-dev"

        resp = requests.get(
            urljoin(
                self.target_endpoint,
                str(Path(workspace_endpoint).joinpath("analytics")),
            ),
            params={"auth_code": auth_code, "name": name},
        )

        if resp.ok:
            resp = resp.json()
            if resp:
                message = {"message": "Find analytic app {0}, update now".format(name)}
                print(message)
                push_url = Path(workspace_endpoint).joinpath(
                    "analytics", resp[0]["uuid"]
                )
            else:
                message = {
                    "message": "Create new analytic app with name {0}".format(name)
                }
                print(message)
                push_url = Path(workspace_endpoint).joinpath("analytics")

        archive = BytesIO()
        with ZipFile(archive, mode="w", compression=ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    path = root.split(str(source_path))[1]
                    zip_file.write(
                        Path(root).joinpath(file), arcname=Path(path).joinpath(file)
                    )

        archive.seek(0)
        files = {"archive": ("archive.zip", archive, "application/zip")}
        resp = requests.put(
            urljoin(self.target_endpoint, str(push_url)),
            files=files,
            params={"auth_code": auth_code},
            timeout=None,
        )

        if not resp.ok:
            message = {"error": "Push analytic app filed", "response": resp.text}
            raise Exception(message)
