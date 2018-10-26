import logging
import urllib3
from afs.get_env import AfsEnv
import afs.utils as utils
import requests
import traceback
import warnings

_logger = logging.getLogger(__name__)

class services(object):

    def __init__(self, target_endpoint=None, instance_id=None, auth_code=None):
        """
        The module can get the credential or the subscribed service.
        """
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        envir = AfsEnv(
            target_endpoint=target_endpoint,
            instance_id=instance_id,
            auth_code=auth_code)
        self.target_endpoint = envir.target_endpoint
        self.instance_id = envir.instance_id
        self.auth_code = envir.auth_code
        self.entity_uri = 'services'


    def get_service_info(self, service_name, service_key=None):
        """
        Get the subscribed service one of key.

        :param str service_name:  (required) service name
        """
        try:
            resp = self._get().json()
        except Exception as e:
            raise AssertionError('Failed to connect API server.')
            traceback.print_exc()

        service_list = [service for service in resp
                        if service['name'] == service_name]

        if len(service_list) == 0:
            warnings.warn('The service whose name is {} and type is {} is not exist.'.format(service_name, service_type))
            return {}

        key_list = [key for key in service_list[0]['service_keys']]
        if len(service_list) == 0:
            warnings.warn('The key in your service is empty.'.format(service_name, service_type))
            return {}

        if service_key is None:
            credential = [list(cre.values())[0] for cre in key_list]
            if len(credential) == 0:
                warnings.warn('There is no key exist.'.format(service_key))
                return {}
        else:
            credential = [list(cre.values())[0] for cre in key_list if list(cre.keys())[0] == service_key]
            if len(credential) == 0:
                warnings.warn('Key {} is not exist.'.format(service_key))
                return {}

        return credential[0]


    def get_service_list(self):
        """
        List all credentials which the services you subscribed.

        :return: list. credential info
        """

        try:
            resp = self._get().json()
        except Exception as e:
            raise AssertionError('Failed to connect API server.')
            traceback.print_exc()

        return resp


    def _get(self, params={}, extra_paths=[]):
        if len(extra_paths) == 0:
            url = '%s%s/%s' % (self.target_endpoint, self.instance_id,
                               self.entity_uri)
        else:
            url = '%s%s/%s/%s' % (self.target_endpoint, self.instance_id,
                                  self.entity_uri, '/'.join(extra_paths))
        get_params = {}
        get_params.update(dict(auth_code=self.auth_code))
        get_params.update(params)
        response = utils._check_response(
            requests.get(url, params=get_params, verify=False))
        _logger.debug('GET - %s - %s', url, response.text)
        return response


# if __name__=='__main__':
#     services_resource = services("https://portal-afs-develop.iii-arfa.com/",  "70c2d65c-1f91-4607-843d-12b90a4faa7b", "CpSmlfe-J4RGZmoaF607fA")
#     resp = services_resource.get_service_info()
#     assert resp is not {}
#     assert 'influxdb' in resp
#     print('test finish')