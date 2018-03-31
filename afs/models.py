import json
import logging
import os
from io import BytesIO
import requests
from afs.utils import InvalidStatusCode

_logger = logging.getLogger(__name__)

class models(object):
    def __init__(self, target_endpoint, instance_id, auth_code, entity_uri):
        self.target_endpoint = target_endpoint
        self.instance_id = instance_id
        self.auth_code = auth_code
        self.entity_uri = entity_uri
        self.repo_id = None

    def _download_model(model_path, afs_config):
        download_url = afs_config['afs_url'] + 'v1/' + afs_config['instance_id'] + '/models/' + afs_config['repo_id'] + '/download'
        result = requests.get(download_url, params={'auth_code': afs_config['auth_code']},)
        with open(model_path, 'wb') as f:
             f.write(result.content)
        f.close()

    def upload_model(self, model_name, accuracy, loss, tags={}, extra_evaluation={}):
        """
         :rtype: None
         :param model_name:  (required) string, model path or name
         :param accuracy: (required) float, model accuracy value
         :param loss: (required) float, model loss value
         :param tags: (optional) dict, tag from model
         :param extra_evaluation: (optional) dict, other evaluation from model
         """
        if os.path.exists(model_name) is False:
            raise AssertionError('File %s is not exist.' % model_name)
        if type(accuracy) is not float or type(loss) is not float:
            raise AssertionError('Accuacy or loss value is not float.' % model_name)

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
        f.close()
        resp = self._put(data=data, files=files, extra_paths=extra_paths)

    def _create_model_repo(self, repo_name):
        request = dict(name=repo_name)
        resp = self._create(request)
        # self.repo_id = resp.json()['uuid']
        return resp.json()['uuid']

    def _get_model_list(self, repo_name=None):
        print(self.target_endpoint, self.instance_id, self.auth_code)
        params = dict(name=repo_name)
        return self._get(params=params)

    def _is_repo_exist(self, repo_name=None):
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

    def _get(self, params={}, requested_path=''):
        url = '%s%s/%s%s' % (self.target_endpoint, self.instance_id, self.entity_uri, requested_path)
        get_params = {}
        get_params.update(dict(auth_code=self.auth_code))
        get_params.update(params)
        response = models._check_response(requests.get(url, params=get_params ))
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



