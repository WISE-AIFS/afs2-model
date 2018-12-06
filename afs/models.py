import json
import logging
import os
from io import BytesIO
import requests
import afs.utils as utils
from afs.get_env import AfsEnv
import re

_logger = logging.getLogger(__name__)

class models(object):
    def __init__(self, target_endpoint=None, instance_id=None, auth_code=None):
        """
        Connect to afs models service, user can connect to service by enviroment parameter. Another way is input when created.
        """
        envir = AfsEnv(
            target_endpoint=target_endpoint,
            instance_id=instance_id,
            auth_code=auth_code)
        self.target_endpoint = envir.target_endpoint
        self.instance_id = envir.instance_id
        self.auth_code = envir.auth_code
        self.api_version = envir.api_version
        if self.api_version == 'v1':
            self.entity_uri = 'models'
        elif self.api_version == 'v2':
            self.entity_uri = 'model_repositories'
        self.repo_id = None

    def _download_model(self, save_path):
        if self.repo_id is not None:
            extra_paths = [self.repo_id, 'download']
            resp = self._get(extra_paths=extra_paths)
            with open(save_path, 'wb') as f:
                f.write(resp.content)
        else:
            AssertionError('There is no specific repo id to download.')

    def download_model(self, save_path, model_name=None):
        """Download model from model repository to a file.

        :param str model_name: The model name exists in model repository
        :param str save_path: The path exist in file system
        """
        if model_name is not None:
            self.repo_id = self.switch_repo(model_name)
        if self.repo_id is None:
            AssertionError('The model repository is not existed')
        else:
            self._download_model(save_path)

    def upload_model(self,
                     model_name,
                     accuracy,
                     loss,
                     tags={},
                     extra_evaluation={}):
        """
        Upload model_name to model repository.If model_name is not exists in the repository, this function will create one.(Support v2 API)

        :param str model_name:  (required) model path or name
        :param float accuracy: (required) model accuracy value, between 0-1
        :param float loss: (required) model loss value
        :param dict tags: (optional) tag from model
        :param dict extra_evaluation: (optional) other evaluation from model
        :return: bool or exception
        """

        if not isinstance(accuracy, float) or \
                not isinstance(loss, float) or \
                not isinstance(tags, dict) or \
                not isinstance(extra_evaluation, dict):
            raise AssertionError(
                'Type error, accuracy and loss are float, and tags and extra_evaluation are dict.'
            )

        if not isinstance(model_name, str):
            raise AssertionError('Type error, model_name  cannot convert to string')

        if not os.path.isfile(model_name):
            raise AssertionError('File not found, model path is not exist.')

        else:
            model_path = model_name
            if os.path.sep in model_name:
                model_name = model_name.split(os.path.sep)[-1]

            if len(model_name) > 42 or len(model_name) < 1:
                raise AssertionError('Model name length  is upper limit 1-42 char')

            pattern = re.compile(r'(?!.*[^a-zA-Z0-9-_.]).{1,42}')
            match = pattern.match(model_name)
            if match is None:
                raise AssertionError('Model naming rule is only a-z, A-Z, 0-9, - and _ allowed.')

        if os.path.getsize(model_name) > 2*(1024*1024*1024):
            raise AssertionError('Model size is upper limit 2 GB.')

        with open(model_path, 'rb') as f:
            model_file = BytesIO(f.read())
        model_file.seek(0)
        self.repo_id = self.switch_repo(model_name)
        if self.repo_id is None:
            self.repo_id = self.create_model_repo(model_name)

        if accuracy > 1.0 or accuracy < 0:
            raise AssertionError('Accuracy value should be between 0-1')

        evaluation_result = {'accuracy': accuracy, 'loss': loss}
        evaluation_result.update(extra_evaluation)
        data = dict(
            tags=json.dumps(tags),
            evaluation_result=json.dumps(evaluation_result))
        files = {'model': model_file}
        extra_paths = [self.repo_id, 'upload']
        resp = self._put(data=data, files=files, extra_paths=extra_paths)

        if int(resp.status_code / 100) == 2:
            return True
        else:
            return False

    def create_model_repo(self, repo_name):
        """
        Create a new model repository. (Support v2 API)
        
        :param str repo_name: (optional)The name of model repository.
        :return: the new uuid of the repository
        """
        if isinstance(repo_name, str):
            if len(repo_name) > 42 or len(repo_name) < 1:
                raise AssertionError('Model name length  is upper limit 1-42 char')
            pattern = re.compile(r'(?!.*[^a-zA-Z0-9-_.]).{1,42}')
            match = pattern.match(repo_name)
            if match is None:
                raise AssertionError('Model naming rule is only a-z, A-Z, 0-9, - and _ allowed.')
        else:
            raise AssertionError('Repo name must be string')

        request = dict(name=repo_name)
        resp = self._create(request)
        return resp.json()['uuid']


    def _get_model_list(self, repo_name=None):
        params = dict(name=repo_name)
        return self._get(params=params)


    def switch_repo(self, repo_name=None):
        """
        Switch current repository. If the model is not exist, return none. (Support v2 API)

        :param str repo_name: (optional)The name of model repository.
        :return: None, repo_id, exception
        """
        params = dict(name=repo_name)
        resp = self._get(params=params)
        if len(resp.json()) == 0:
            return None
        elif len(resp.json()) == 1:
            self.repo_id = resp.json()[0]['uuid']
            return self.repo_id
        else:
            raise ValueError('There are multi model repositories from server response')


    def get_latest_model_info(self, repo_name=None):
        """
        Get the latest model info, including created_at, tags, evaluation_result. (Support v2 API)
        
        :param repo_name: (optional)The name of model repository.
        :return: dict. the latest of model info in model repository.
        """
        if repo_name:
            self.switch_repo(repo_name)

        if self.api_version == 'v1':
            resp = self._get(extra_paths=[self.repo_id, 'info'])
        elif self.api_version == 'v2':
            resp = self._get(extra_paths=[self.repo_id, 'last'])
        return resp.json()


    def _create(self, data, files=None, extra_paths=[]):
        if self.api_version == 'v1':
            if len(extra_paths) == 0:
                url = '%s%s/%s' % (self.target_endpoint, self.instance_id,
                                   self.entity_uri)
            else:
                url = '%s%s/%s/%s' % (self.target_endpoint, self.instance_id,
                                      self.entity_uri, '/'.join(extra_paths))
        elif self.api_version == 'v2':
            url = utils.urljoin(self.target_endpoint, 'instances', self.instance_id, self.entity_uri,
                                 extra_paths=extra_paths)

        if not files:
            response = utils._check_response(
                requests.post(
                        url,
                        params=dict(auth_code=self.auth_code),
                        json=data,
                        verify=False))
        else:
            response = utils._check_response(
                    requests.post(
                        url,
                        params=dict(auth_code=self.auth_code),
                        json=data,
                        files=files,
                        verify=False))
        _logger.debug('POST - %s - %s', url, response.text)
        return response



    def _put(self, data, files=None, extra_paths=[]):
        if self.api_version == 'v1':
            if len(extra_paths) == 0:
                url = '%s%s/%s' % (self.target_endpoint, self.instance_id,
                                   self.entity_uri)
            else:
                url = '%s%s/%s/%s' % (self.target_endpoint, self.instance_id,
                                      self.entity_uri, '/'.join(extra_paths))
        elif self.api_version == 'v2':
            url = utils.urljoin(self.target_endpoint, 'instances' ,self.instance_id, self.entity_uri, extra_paths=extra_paths)

        if not files:
            response = utils._check_response(
                requests.put(
                        url,
                        params=dict(auth_code=self.auth_code),
                        data=data,
                        verify=False))
        else:
            response = utils._check_response(
                requests.put(
                        url,
                        params=dict(auth_code=self.auth_code),
                        files=files,
                        data=data,
                        verify=False))
        _logger.debug('PUT - %s - %s', url, response.text)
        return response


    def _get(self, params={}, extra_paths=[]):
        if self.api_version == 'v1':
                if len(extra_paths) == 0:
                    url = '%s%s/%s' % (self.target_endpoint, self.instance_id,
                                       self.entity_uri)
                else:
                    url = '%s%s/%s/%s' % (self.target_endpoint, self.instance_id,
                                          self.entity_uri, '/'.join(extra_paths))
        elif self.api_version == 'v2':
            url = utils.urljoin(self.target_endpoint, 'instances', self.instance_id, self.entity_uri,
                                 extra_paths=extra_paths)

        get_params = {}
        get_params.update(dict(auth_code=self.auth_code))
        get_params.update(params)
        response = utils._check_response(
        requests.get(url, params=get_params, verify=False))
        _logger.debug('GET - %s - %s', url, response.text)
        return response
