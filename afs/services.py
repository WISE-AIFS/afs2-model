import logging
import urllib3
from afs.get_env import AfsEnv
import afs.utils as utils
import requests

_logger = logging.getLogger(__name__)

class services(object):

    def __init__(self, target_endpoint=None, instance_id=None, auth_code=None):
        """
        Connect to afs models service, user can connect to service by enviroment parameter. Another way is input when created.
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
        self.repo_id = None

    # def get_service_info(self, service=None, specific_key=None):
    def get_service_info(self):

        try:
            resp = self._get().json()
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
                        username = service_key[key]['username']
                        password = service_key[key]['password']
                        host = service_key[key]['host']
                        database = service_key[key]['database']
                        port = service_key[key]['port']
                        uri = service_key[key]['uri']
                        info = dict(key=key, username=username, password=password, host=host, database=database,
                                    port=port,
                                    uri=uri, service_name=service_name, service_type=service_type)
                        service_keys_info_list.append(info)
                else:
                    pass
                service_info[service_type] = service_keys_info_list

                # if service:
                #     if specific_key:
                #         for service_key_info in service_info[service]:
                #             print(service_key_info['key'])
                #             if specific_key is service_key_info['key']:
                #                 return service_key_info
                #         else:
                #             raise AssertionError('key not found')
                #     else:
                #         return {service: service_info[service]}

            return service_info
        except Exception as e:
            print(e)
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


if __name__=='__main__':
    services_resource = services("https://portal-afs-develop.iii-arfa.com/",  "779fd10d-24ee-4603-b18a-dcb279eac8b5", "iV8KIPe3nG0aAH2FBrhRMQ")
    resp = services_resource.get_service_info()
    print(resp['influxdb'])