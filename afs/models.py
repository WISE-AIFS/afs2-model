import json
import logging
import os
from io import BytesIO
import requests
import afs.utils as utils
from afs.get_env import AfsEnv
import re
from uuid import uuid4


_logger = logging.getLogger(__name__)

class models(object):

    def __init__(self, target_endpoint=None, instance_id=None, auth_code=None):
        """Connect to afs models service, user can connect to service by enviroment parameter. Another way is input when created.
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
            self.sub_entity_uri = 'models'
        self.repo_id = None


    def get_model_repo_id(self, model_repository_name=None):
        """Get model repository by name.
        
        :param str model_repository_name:  
        :return: str model repository id
        """
        if self.api_version == 'v2':
            if model_repository_name:
                params = dict(name=model_repository_name)
                resp = self._get(params=params).json()

                if resp['resources']:
                    repo_id = resp['resources'][0]['uuid']
                else:
                    self.repo_id = None
                    return None
                self.repo_id = repo_id
        else:
            raise NotImplementedError('v1 API is not support this method.')
            return None

        return self.repo_id


    def get_model_id(self, model_name=None, model_repository_name=None, last_one=True):
        """Get model id by model name.
        
        :param str model_name: model name. No need if last_one is true.
        :param str model_repository_name: model respository name where the model is.
        :param bool last_one: auto get the model_repository last one model
        :return: str model id
        """
        if self.api_version == 'v2':

            if not model_repository_name:
                if not self.repo_id:
                    raise ValueError('Please enter model_repository_name.')
            else:
                self.repo_id = self.get_model_repo_id(model_repository_name)
                if not self.repo_id:
                    raise ValueError('Model_repository_name {} not found.'.format(model_repository_name))

            if last_one:
                extra_paths = [self.repo_id, self.sub_entity_uri]
                resp = self._get(extra_paths=extra_paths).json()
            elif model_name:
                params = dict(name=model_name)
                extra_paths = [self.repo_id, self.sub_entity_uri]
                resp = self._get(extra_paths=extra_paths, params=params).json()
            else:
                raise ValueError('It must be one of model_name or last_one')
                return None

            if resp['resources']:
                model_id = resp['resources'][0]['uuid']
            else:
                return None
            return model_id
        else:
            raise NotImplementedError('v1 API is not support this method.')
            return None


    def download_model(self, save_path, model_repository_name=None, model_name=None, last_one=False):
        """Download model from model repository to a file.

        :param str model_repository_name: The model name exists in model repository
        :param str save_path: The path exist in file system
        """
        if model_repository_name:
            self.repo_id = self.get_model_repo_id(model_repository_name)

        if not self.repo_id:
            raise ValueError('There is no specific repo_id to download.')

        if self.api_version in 'v1':
            extra_paths = [self.repo_id, 'download']
            resp = self._get(extra_paths=extra_paths)

        elif self.api_version in 'v2':
            model_id = self.get_model_id(model_name=model_name, model_repository_name=model_repository_name, last_one=last_one)
            if model_id:
                extra_paths = [self.repo_id, self.sub_entity_uri, model_id]
                params = {'alt': 'media'}
                resp = self._get(params=params, extra_paths=extra_paths)
            else:
                raise ValueError('Model_name {} not found.'.format(model_name))

        try:
            with open(save_path, 'wb') as f:
                f.write(resp.content)
        except Exception as e:
            raise RuntimeError('Write download file error.')
            return False

        return True


    def upload_model(self,
                     model_path,
                     accuracy,
                     loss,
                     tags={},
                     extra_evaluation={},
                     model_repository_name=None,
                     model_name=None):
        """
        Upload model_name to model repository.If model_name is not exists in the repository, this function will create one.(Support v2 API)

        :param str model_path:  (required) model path 
        :param float accuracy: (required) model accuracy value, between 0-1
        :param float loss: (required) model loss value
        :param dict tags: (optional) tag from model
        :param dict extra_evaluation: (optional) other evaluation from model
        :param str model_path:  (optional) Give model a name or default auto a uuid4 name 

        :return: bool
        """

        if not isinstance(accuracy, float) or \
                not isinstance(loss, float) or \
                not isinstance(tags, dict) or \
                not isinstance(extra_evaluation, dict):
            raise AssertionError(
                'Type error, accuracy and loss are float, and tags and extra_evaluation are dict.'
            )

        if not isinstance(model_path, str):
            raise AssertionError('Type error, model_name  cannot convert to string')

        if not os.path.isfile(model_path):
            raise AssertionError('File not found, model path is not exist.')
        else:
            model_path = model_path
            if os.path.sep in model_path:
                model_path = model_path.split(os.path.sep)[-1]

            if len(model_path) > 42 or len(model_path) < 1:
                raise AssertionError('Model name length  is upper limit 1-42 char')

            pattern = re.compile(r'(?!.*[^a-zA-Z0-9-_.]).{1,42}')
            match = pattern.match(model_path)
            if match is None:
                raise AssertionError('Model naming rule is only a-z, A-Z, 0-9, - and _ allowed.')

        # Check file size
        if os.path.getsize(model_path) > 2*(1024*1024*1024):
            raise AssertionError('Model size is upper limit 2 GB.')

        with open(model_path, 'rb') as f:
            model_file = BytesIO(f.read())
        model_file.seek(0)

        if self.api_version in 'v1':
            self.repo_id = self.switch_repo(model_path)
            if not self.repo_id:
                self.repo_id = self.create_model_repo(model_path)
        elif self.api_version == 'v2':
            # Check default repo_id
            if not self.repo_id:
                # Find model_repo_id from name
                if model_repository_name:
                    self.repo_id = self.get_model_repo_id(model_repository_name)
                    # If not found, create one
                    if not self.repo_id:
                        self.repo_id = self.create_model_repo(model_repository_name)
                else:
                    raise ValueError('Please enter model_repository_name')

        if accuracy >= 1.0 or accuracy < 0:
            raise AssertionError('Accuracy value should be between 0-1')

        # tag info
        evaluation_result = {'accuracy': accuracy, 'loss': loss}

        # evaluation result
        evaluation_result.update(extra_evaluation)
        data = dict(
            tags=json.dumps(tags),
            evaluation_result=json.dumps(evaluation_result))
        files = {'model': model_file}

        if self.api_version in 'v1':
            extra_paths = [self.repo_id, 'upload']
            resp = self._put(data=data, files=files, extra_paths=extra_paths)

        elif self.api_version == 'v2':
            if not model_name:
                data.update({'name': str(uuid4())})

            extra_paths = [self.repo_id, self.sub_entity_uri]
            resp = self._create(data=data, files=files, extra_paths=extra_paths, form='data')

        if int(resp.status_code / 100) == 2:
            return True
        else:
            return False


    def create_model_repo(self, model_repository_name):
        """
        Create a new model repository. (Support v2 API)
        
        :param str repo_name: (optional)The name of model repository.
        :return: the new uuid of the repository
        """
        if isinstance(model_repository_name, str):
            if len(model_repository_name) > 42 or len(model_repository_name) < 1:
                raise AssertionError('Model name length  is upper limit 1-42 char')
            pattern = re.compile(r'(?!.*[^a-zA-Z0-9-_.]).{1,42}')
            match = pattern.match(model_repository_name)
            if match is None:
                raise AssertionError('Model naming rule is only a-z, A-Z, 0-9, - and _ allowed.')
        else:
            raise AssertionError('Repo name must be string')

        request = dict(name=model_repository_name)
        resp = self._create(request)
        self.repo_id = resp.json()['uuid']
        return self.repo_id


    def switch_repo(self, repo_name=None):
        """
        Switch current repository. If the model is not exist, return none. (Support v2 API)

        :param str repo_name: (optional)The name of model repository.
        :return: None, repo_id, exception
        """
        if self.api_version == 'v2':
            params = dict(name=repo_name)
            resp = self._get(params=params)
            if len(resp.json()) == 0:
                return None
            elif len(resp.json()) == 1:
                self.repo_id = resp.json()[0]['uuid']
                return self.repo_id
            else:
                raise ValueError('There are multi model repositories from server response')
        else:
            raise NotImplementedError('v2 API is not support this method.')
            return None

    def get_latest_model_info(self, model_repository_name=None):
        """
        Get the latest model info, including created_at, tags, evaluation_result. (Support v2 API)
        
        :param model_repository_name: (optional)The name of model repository.
        :return: dict. the latest of model info in model repository.
        """
        if self.api_version == 'v1':
            if model_repository_name:
                self.switch_repo(model_repository_name)
            resp = self._get(extra_paths=[self.repo_id, 'info'])

        elif self.api_version == 'v2':
            model_id = self.get_model_id(model_repository_name=model_repository_name, last_one=True)

            if model_id:
                extra_paths = [self.repo_id, self.sub_entity_uri, model_id]
                resp = self._get(extra_paths=extra_paths)
                resource = resp.json()['resources'][0]
                return resource
            else:
                raise ValueError('Model not found.')
                return None

    def get_model_info(self, model_name, model_repository_name=None):
        """Get model info, including created_at, tags, evaluation_result. (V2 API)
        
        :param model_name: model name
        :param model_repository_name: The name of model repository.
        :return: dict model info
        """
        if self.api_version == 'v2':
            if not self.get_model_repo_id(model_repository_name=model_repository_name):
                raise ValueError('Model_repository not found.')

            model_id = self.get_model_id(model_name=model_name, model_repository_name=model_repository_name)

            if model_id:
                extra_paths = [self.repo_id, self.sub_entity_uri, model_id]
                resp = self._get(extra_paths=extra_paths)
            else:
                raise ValueError('Model not found.')
        else:
            raise NotImplementedError('v1 API is not support this method.')
            return None
        return resp.json()


    def delete_model_repository(self, model_repository_name):
        """Delete model repository.
        
        :param model_repository_name: model repository name.
        :return: bool 
        """
        if self.api_version == 'v2':
            if not self.get_model_repo_id(model_repository_name):
                raise ValueError('Model_repository not found.')
                return False
            extra_paths = [self.repo_id]
            resp = self._del(extra_paths=extra_paths)

        else:
            raise NotImplementedError('v1 API is not support this method.')
            return None

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
        if self.api_version == 'v2':
            if not self.get_model_repo_id(model_repository_name=model_repository_name):
                raise ValueError('Model_repository not found.')
                return False
            model_id = self.get_model_id(model_name, model_repository_name=model_repository_name, last_one=False)
            if not model_id:
                raise ValueError('Model not found.')
            extra_paths = [self.repo_id, self.sub_entity_uri, model_id]
            resp = self._del(extra_paths=extra_paths)
        else:
            raise NotImplementedError('v1 API is not support this method.')
            return None

        if int(resp.status_code / 100) == 2:
            return True
        else:
            return False


    def _create(self, data, files=None, extra_paths=[], form='json'):

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
            if form in 'json':
                response = utils._check_response(
                        requests.post(
                            url,
                            params=dict(auth_code=self.auth_code),
                            json=data,
                            files=files,
                            verify=False))
            elif form in 'data':
                response = utils._check_response(
                    requests.post(
                        url,
                        params=dict(auth_code=self.auth_code),
                        data=data,
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


    def _del(self, params={}, extra_paths=[]):
        url = utils.urljoin(self.target_endpoint, 'instances', self.instance_id, self.entity_uri,
                            extra_paths=extra_paths)

        get_params = {}
        get_params.update(dict(auth_code=self.auth_code))
        get_params.update(params)
        response = utils._check_response(
            requests.delete(url, params=get_params, verify=False))
        _logger.debug('DELETE - %s - %s', url, response.text)
        return response
