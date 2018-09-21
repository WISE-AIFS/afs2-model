import os, json
import requests

class AfsEnv():
    def __init__(self, target_endpoint=None, instance_id=None, auth_code=None):
        if target_endpoint is None or instance_id is None or auth_code is None:
            self.target_endpoint = os.getenv('afs_url', None)
            self.auth_code = os.getenv('auth_code', None)
            vcap = json.loads(os.getenv('VCAP_APPLICATION', {}))
            if not vcap:
                raise AssertionError('Environment VCAP_APPLICATION is empty')
            self.instance_id = vcap.get('space_name', None)

            if self.target_endpoint == None or self.instance_id == None or self.auth_code == None:
                raise AssertionError('Environment parameters need afs_url, instance_id, auth_code')
        else:
            self.target_endpoint = target_endpoint
            self.auth_code = auth_code
            self.instance_id = instance_id

        if not self.target_endpoint.endswith('/'):
            self.target_endpoint = self.target_endpoint + '/'
        self.target_endpoint = self.target_endpoint + 'v1/'

class app_env(object):
    def __init__(self):
        # VCAP_APPLICATION
        if os.getenv('VCAP_APPLICATION') is None:
            self._app = {}
        else:
            self._app = json.loads(os.getenv('VCAP_APPLICATION'))

        # afs_host_url
        if os.getenv('afs_url') is None:
            self._afs_host_url = None
        else:
            self._afs_host_url = self.format_url(str(os.getenv('afs_url')))

        # node_host_url
        if os.getenv('node_red_url') is None:
            self._node_host_url = None
        else:
            self._node_host_url = self.format_url(str(os.getenv('node_red_url')))

        # afs_auth_code
        if os.getenv('auth_code') is None:
            self._afs_auth_code = None
        else:
            self._afs_auth_code = str(os.getenv('auth_code'))

        # get param from AFS api
        self._param_obj = self.get_required_param()

        # sso_host_url
        if os.getenv('sso_host_url') is None:
            # self._sso_host_url = None
            try:
                self._sso_host_url = self._param_obj.get('sso_host_url')  # get from afs api
            except Exception as err:
                print('Get sso host url error occur.')
                self._sso_host_url = None
        else:
            self._sso_host_url = self.format_url(str(os.getenv('sso_host_url')))

        # rmm_host_url
        if os.getenv('rmm_host_url') is None:
            # self._rmm_host_url = None
            try:
                self._rmm_host_url = self._param_obj.get('rmm_host_url')  # get from afs api
            except Exception as err:
                print('Get rmm host url error occur.')
                self._rmm_host_url = None
        else:
            self._rmm_host_url = self.format_url(str(os.getenv('rmm_host_url')))

    def get_required_param(self, host_url=None):
        """
        Requrest AFS api to get other required param.
        {sso_host_url, rmm_host_url}

        :param  host_url    (string)
        :return param_obj   (dict) Response from AFS api. If exception occurs, response None.
        """
        # if host_url is None use self._afs_host_url
        host_url = self.format_url(host_url) if host_url is not None else self._afs_host_url
        param_obj = None
        str_url = host_url + '/v1/' + self.vcap_app.get('space_name') + '/workspaces/' + self.vcap_app.get(
            'space_id') + '/env?auth_code=' + self.afs_auth_code
        # print(str_url)
        headers_obj = {
            'Authorization': self.afs_auth_code
        }

        # request AFS api
        try:
            result = requests.get(str_url, headers=headers_obj, timeout=5)
        except Exception as err:
            print('Request AFS api: ' + str(err))
            return None

        # status code not success
        if result.status_code != requests.codes.ok:
            print('Request AFS api get env variable status code: ' + str(result.status_code))
            return None

        # parse json
        try:
            param_obj = json.loads(result.text)  # trans POST response to json
        except Exception as err:
            print('Request AFS api: ' + str(err))
            return None

        return param_obj

    def format_url(self, url):
        """
        Format url without / at last character.

        :param  string  url: url before format.
        :return string  f_url: url after format.
        """
        f_url = ''

        if not url.endswith('/'):
            f_url = url
        else:
            f_url = url[:-1]  # remove last character

        return f_url

    @property
    def vcap_app(self):
        return self._app

    @vcap_app.setter
    def vcap_app(self, obj):
        self._app = json.loads(str(obj))

    @property
    def afs_host_url(self):
        return self._afs_host_url

    @afs_host_url.setter
    def afs_host_url(self, url):
        self._afs_host_url = self.format_url(url)
        # self._afs_host_url = url

    @property
    def node_host_url(self):
        return self._node_host_url

    @node_host_url.setter
    def node_host_url(self, url):
        self._node_host_url = self.format_url(url)
        # self._node_host_url = url

    @property
    def afs_auth_code(self):
        return self._afs_auth_code

    @afs_auth_code.setter
    def afs_auth_code(self, value):
        self._afs_auth_code = value

    @property
    def sso_host_url(self):
        return self._sso_host_url

    @sso_host_url.setter
    def sso_host_url(self, url):
        self._sso_host_url = self.format_url(url)
        # self._sso_host_url = url

    @property
    def rmm_host_url(self):
        return self._rmm_host_url

    @rmm_host_url.setter
    def rmm_host_url(self, url):
        self._rmm_host_url = self.format_url(url)
        # self._rmm_host_url = url