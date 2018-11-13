import json
from pandas import DataFrame
from afs.flow import flow
import logging
import os
from pathlib import Path
import afs


_logger = logging.getLogger(__name__)

class config_handler(object):

    def __init__(self):
        """
        Config handler is the class which handle AFS flow framework. User can use function fetch parameters, or send data to next node.
        """
        self.param = []
        self.variable_name = []
        self.column = []
        self.features = False
        self.data = DataFrame.empty
        self.type_list = {'string': str, 'integer': int, 'float': float, 'list': list}
        self.REQUEST = None
        self.headers = None
        self.token = None
        self.smry = None

    def set_kernel_gateway(self, REQUEST, flow_json_file=None, env_obj={}):
        """
        For Jupyter kernel gateway API, REQUEST is the request given by kernel gateway. Reference REQUEST: http://jupyter-kernel-gateway.readthedocs.io/en/latest/http-mode.html

        :param str REQUEST: Jupyter kernel gateway request.
        :param dict env_obj: Key names are VCAP_APPLICATION, afs_host_url, node_host_url, afs_auth_code, sso_host_url, rmm_host_url(option).
        :param str flow_json_file: String of file path. For debug, developer can use file which contains the flow json as the flow json gotten from NodeRed.
        """

        if not isinstance(REQUEST, str):
            raise TypeError("REQUEST must be the string of json format")

        try:
            self.REQUEST = json.loads(REQUEST)
        except Exception as e:
            raise TypeError('REQUEST must be json format.')

        self.headers = self.REQUEST.get('headers')
        if self.headers is None:
            raise KeyError('header not found')

        node_id = self.headers.get('Node_id')
        if node_id is None:
            raise KeyError('Node id not found.')
        if not node_id:
            raise ValueError('Node id can not be empty')

        flow_id = self.headers.get('Flow_id')
        if flow_id is None:
            raise KeyError('Flow id not found.')
        if not flow_id:
            raise ValueError('Flow id can not be empty')

        afs_url = self.headers.get('afs_url')
        if afs_url:
            os.environ['afs_url'] = afs_url

        instance_id = self.headers.get('instance_id')
        if instance_id:
            os.environ['instance_id'] = instance_id

        auth_code = self.headers.get('auth_code')
        if auth_code:
            os.environ['auth_code'] = auth_code

        workspace_id = self.headers.get('workspace_id')
        if workspace_id:
            os.environ['workspace_id'] = workspace_id

        nodered_url = self.headers.get('node_host_url')
        if nodered_url:
            os.environ['node_host_url'] = nodered_url

        afs_portal_version = afs._get_portal_version()
        if afs_portal_version:
            os.environ['version'] = afs_portal_version

        self.flow_obj = flow(env_obj=env_obj)
        self.flow_obj.set_flow_config({'flow_id': flow_id, 'node_id': node_id})

        if flow_json_file:
            try:
                flow_json = json.loads(flow_json_file)
                self.flow_obj.get_flow_list_ab(flow_json)
            except Exception as e:
                raise TypeError('Type error, flow_json must be JSON(For nodered request type not UI type)')
        else:
            try:
                self.flow_obj.get_flow_list()
            except Exception as e:
                raise RuntimeError('Request to NodeRed has porblem.')

        # get the node information in current_node_obj
        self.flow_obj.get_node_item(self.flow_obj.current_node_id)

    def get_param(self, key):
        """
        Get parameter from the key name, and it should be set from set_param.

        :param str key: The parameter key set from method set_param
        :return: Specfic type depends on set_param. The value of the key name.
        """
        obj_value = self.flow_obj.current_node_obj[key]
        obj_para = [x for x in self.param if x['name'] in key][0]
        try:
            if obj_para['type'] in 'integer':
                obj_value = int(obj_value)
            elif obj_para['type'] in 'string':
                obj_value = str(obj_value)
            elif obj_para['type'] in 'float':
                obj_value = float(obj_value)
            elif obj_para['type'] in 'list:':
                obj_value = json.loads(obj_value)
                if not isinstance(obj_value, list):
                    message = {
                        'error': 'Type of {0} is not list.'.format(key)
                    }
                    raise Exception(message)
            else:
                _logger.warning('Parameter has no specific type.')
                obj_value = str(obj_value)
        except Exception as e:
            raise ValueError('The value has problem to change type.')

        if obj_value:
            return obj_value
        else:
            return None

    def get_data(self):
        """
        Transform REQUEST data to DataFrame type.

        :return: DataFrame type. Data from REQUEST and rename column name.
        """

        if self.REQUEST is None:
            raise RuntimeError('set_kernel_gateway should be shown before this method.')

        body = self.REQUEST.get('body')
        if body is None:
                raise KeyError('Request contains no key named "data"')
        if not body:
            raise ValueError

        data = body.get('data')
        if data is None:
            raise KeyError
        if not data:
            raise ValueError

        try:
            self.data = DataFrame.from_dict(data)
        except Exception as e:
            raise ValueError('Request data cannot transform to dataframe type.')

        return self.data.rename(columns=self.get_column())

    def get_column(self):
        """
        Get the column mapping list.

        :return: The value is the column name would use in the AFS API, and the key is the mapping column name.
        :rtype: dict
        """
        return {self.flow_obj.current_node_obj[column_name]: column_name
                for column_name in self.flow_obj.current_node_obj
                if column_name in self.column}

    def next_node(self, data, debug=False):
        """
        Send data to next node according to flow.

        :param data: DataFrame type. Data will be sent to next node.
        :param bool debug: If debug is True, method will return response message from the next node.
        :return: Response JSON
        :rtype: dict
        """
        if isinstance(data, DataFrame):
            column_reverse_mapping = {v: k for k, v in self.get_column().items()}
            data = data.rename(columns=column_reverse_mapping)
            data = dict(data=data.to_dict())
            return self.flow_obj.exe_next_node(data, debug=debug)
        else:
            raise TypeError('data must be DataFrame type')

    def set_param(self, key, type='string', required=False ,default=None):
        """
        Set API parameter will be used in the AFS API.

        :param str key: The key name for this parameter
        :param str type: The type of the paramter, including integer, string or float.
        :param bool required: The parameter is required or not
        :param str default: The parameter is given in default
        """
        # check type in type list
        if type not in self.type_list:
            raise ValueError('Type not found.')
        else:
            # check default type
            if default:
                if not isinstance(default, self.type_list[type]):
                    raise TypeError('Default value is not the specific type.')

        # check required value
        if not isinstance(required, bool):
            raise TypeError('required is true/false.')

        # check if the name is the same, raise error
        if key in self.variable_name:
            raise KeyError('It has already the same name of the parameter.')
        else:
            param = {}
            param['name'] = str(key)
            param['type'] = type
            param['required'] = required
            param['default'] = default
            self.variable_name.append(key)
            self.param.append(param)

    def set_column(self, column_name):
        """
        The column name will be used in the AFS API.

        :param str column_name: The column name used in the following API
        """
        column_name = str(column_name)
        if column_name in self.variable_name:
            raise ValueError('It has already the same column name.')
        else:
            self.variable_name.append(column_name)
            self.column.append(column_name)

    def set_features(self, enable=False):
        """
        The feature name will be used in the AFS API.

        :param list feature_list: The feature name used in the following API
        """
        if isinstance(enable, bool):
            self.features = enable
        else:
            raise TypeError('Type Error enable  is bool type')

    def get_features_target(self):
        """
        Get feature target from flow json.

        :return: feature target name
        :rtype: str
        """
        return self.flow_obj.current_node_obj['target']

    def get_features_selected(self):
        """
        Get feature selected from flow json.

        :return: feature select list
        :rtype: list
        """
        return self.flow_obj.current_node_obj['select_feature']

    def get_features_numerical(self):
        """
        Get feature numerical from flow json.

        :return: feature numerical list
        :rtype: list
        """
        return self.flow_obj.current_node_obj['numerical']

    def summary(self):
        """
        Summary what parameters and column the AFS API need.This method should be called by the last line in the 2nd cell.
        """
        self.smry = {}
        self.smry['features'] = self.features
        self.smry['param'] = self.param
        self.smry['column'] = self.column
        print(json.dumps(self.smry))
