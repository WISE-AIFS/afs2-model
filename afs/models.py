from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import os
from io import BytesIO
import requests
from afs.utils import InvalidStatusCode
from afs.get_env import AfsEnv

_logger = logging.getLogger(__name__)

class models(object):
    def __init__(self, target_endpoint=None, instance_id=None, auth_code=None):
        envir = AfsEnv(target_endpoint=target_endpoint, instance_id=instance_id, auth_code=auth_code)
        self.target_endpoint = envir.target_endpoint
        self.instance_id = envir.instance_id
        self.auth_code = envir.auth_code
        self.entity_uri = 'models'
        self.repo_id = None

    def _download_model(self, model_path):
        if self.repo_id is not None:
            extra_paths = [self.repo_id, 'download' ]
            self._get()


            # download_url = afs_config['afs_url'] + 'v1/' + afs_config['instance_id'] + '/models/' + afs_config['repo_id'] + '/download'
            # result = requests.get(download_url, params={'auth_code': afs_config['auth_code']},)
        with open(model_path, 'wb') as f:
             f.write(result.content)

    def upload_model(self, model_name, accuracy: float, loss: float, tags={}, extra_evaluation={}):
        """
         :rtype: None
         :param model_name:  (required) string, model path or name
         :param accuracy: (required) float, model accuracy value
         :param loss: (required) float, model loss value
         :param tags: (optional) dict, tag from model
         :param extra_evaluation: (optional) dict, other evaluation from model
         """

        if not isinstance(accuracy, float) or not isinstance(loss, float) is not float or not isinstance(tags, dict) or not isinstance(extra_evaluation, dict):
            raise AssertionError('Type error, accuracy and loss is float, and tags and extra_evaluation are dict.')
        try:
            model_name = str(model_name)
        except Exception as e:
            raise AssertionError('Type error, model_name %s cannot convert to string' % (model_name))
        if not os.path.isfile(model_name):
            raise AssertionError('File not found, model %s path is not exist.' % (model_name))
        else:
            if os.path.sep in model_name:
                model_name = model_name.split(os.path.sep)[-1]

        with open(model_name, 'rb') as f:
            model_file = BytesIO(f.read())
        model_file.seek(0)
        resp = self._is_repo_exist(model_name)
        if self.repo_id is None:
            if resp is False:
                self.repo_id = self._create_model_repo(model_name)
            else:
                self.repo_id = resp
        evaluation_result = {'accuracy': accuracy, 'loss': loss}
        evaluation_result.update(extra_evaluation)
        data = dict(tags = json.dumps(tags), evaluation_result = json.dumps(evaluation_result))
        files={'model': model_file}
        extra_paths = [self.repo_id, 'upload']
        resp = self._put(data=data, files=files, extra_paths=extra_paths)

    def _create_model_repo(self, repo_name):
        request = dict(name=repo_name)
        resp = self._create(request)
        return resp.json()['uuid']

    def _get_model_list(self, repo_name=None):
        print(self.target_endpoint, self.instance_id, self.auth_code)
        params = dict(name=repo_name)
        return self._get(params=params)

    def _is_repo_exist(self, repo_name=None):
        """

        :param repo_name
        :return: False or repo_id
        """
        params = dict(name=repo_name)
        resp = self._get(params=params)
        if len(resp.json()) == 0:
            return False
        else:
            self.repo_id = resp.json()[0]['uuid']
            return self.repo_id

    def _create(self, data, files=None, extra_paths=[]):
        if len(extra_paths) == 0:
            url = '%s%s/%s' % (self.target_endpoint, self.instance_id, self.entity_uri)
        else:
            url = '%s%s/%s/%s' % (self.target_endpoint, self.instance_id, self.entity_uri, '/'.join(extra_paths))
        if not files:
            response = models._check_response(requests.post(url, params=dict(auth_code=self.auth_code), json=data))
        else:
            response = models._check_response(requests.post(url, params=dict(auth_code=self.auth_code), json=data, files=files))
        _logger.debug('POST - %s - %s', url, response.text)
        return response

    def _put(self, data, files=None, extra_paths=[]):
        if len(extra_paths) == 0:
            url = '%s%s/%s' % (self.target_endpoint, self.instance_id, self.entity_uri)
        else:
            url = '%s%s/%s/%s' % (self.target_endpoint, self.instance_id, self.entity_uri, '/'.join(extra_paths))
        if not files:
            response = models._check_response(requests.put(url, params=dict(auth_code=self.auth_code), data=data))
        else:
            response = models._check_response(requests.put(url, params=dict(auth_code=self.auth_code), files=files, data=data))
        _logger.debug('PUT - %s - %s', url, response.text)
        return response

    def _get(self, params={}, extra_paths=[]):
        if len(extra_paths) == 0:
            url = '%s%s/%s' % (self.target_endpoint, self.instance_id, self.entity_uri)
        else:
             url = '%s%s/%s/%s' % (self.target_endpoint, self.instance_id, self.entity_uri, '/'.join(extra_paths))
        get_params = {}
        get_params.update(dict(auth_code=self.auth_code))
        get_params.update(params)
        response = models._check_response(requests.get(url, params=get_params))
        _logger.debug('GET - %s - %s', url, response.text)
        return response

    @staticmethod
    def _check_response(response):
        if int(response.status_code / 100) == 2:
            return response
        else:
            try:
                body = response.json()
            except Exception:
                body = response.text
            raise InvalidStatusCode(response.status_code, body)
