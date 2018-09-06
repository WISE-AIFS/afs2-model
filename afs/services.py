import logging
import urllib3
from afs.get_env import AfsEnv
import afs.utils as utils
import requests

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

    # def get_service_info(self, service=None, specific_key=None):
    def get_service_info(self, specific_key=None):
        """
        List all credentials which the services you subscribed.

        :return: dict. The credential info.
        """



        try:
            resp = self._get().json()
        except Exception as e:
            print(e)


        if specific_key != None:
            for service_inst in resp:
                service_keys = service_inst['service_keys']
                for key_pair in service_keys:
                    if specific_key in key_pair:
                        return key_pair[specific_key]
                AssertionError('Key {0} is not existed in any the subscribed service'.format(specific_key))

        try:
            service_info = {}
            for service_inst in resp:
                service_name = service_inst['name']
                service_type = service_inst['service']
                service_keys = service_inst['service_keys']
                service_keys_info_list = []
                if service_keys:
                    for service_key in service_keys:
                        info = {}
                        key = list(service_key.keys())[0]
                        if 'username' in service_key[key]:
                            username = service_key[key]['username']
                        if 'password' in service_key[key]:
                            password = service_key[key]['password']
                        if 'host' in service_key[key]:
                            host = service_key[key]['host']
                        if 'database' in service_key[key]:
                            database = service_key[key]['database']
                        if 'port' in service_key[key]:
                            port = service_key[key]['port']
                        if 'uri' in service_key[key]:
                            uri = service_key[key]['uri']
                        info = dict(key=key, username=username, password=password, host=host, database=database,
                                    port=port,
                                    uri=uri, service_name=service_name, service_type=service_type)
                        service_keys_info_list.append(info)
                else:
                    pass
                service_info[service_type] = service_keys_info_list
            return service_info
        except Exception as e:
            print(e.with_traceback())
            return {}

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