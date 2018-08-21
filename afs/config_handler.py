import json
from pandas import DataFrame
from afs.flow import flow
import logging
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

    def set_kernel_gateway(self, REQUEST, flow_json_file=None, env_obj={}):
        """
        For Jupyter kernel gateway API, REQUEST is the request given by kernel gateway. Reference REQUEST: http://jupyter-kernel-gateway.readthedocs.io/en/latest/http-mode.html

        :param str REQUEST: Jupyter kernel gateway request.
        :param dict env_obj: Key names are VCAP_APPLICATION, afs_host_url, node_host_url, afs_auth_code, sso_host_url, rmm_host_url(option).
        :param str flow_json_file: String of file path. For debug, developer can use file which contains the flow json as the flow json gotten from NodeRed.
        """
        self.flow_obj = flow(env_obj=env_obj)

        try:
            headers = json.loads(REQUEST)['headers']
            flow_info = {}
            flow_info['node_id'] = headers['Node_id']
            flow_info['flow_id'] = headers['Flow_id']
            self.flow_obj.set_flow_config(flow_info)
        except Exception as e:
            raise AssertionError('REQUEST must be json format, or headers contains not enough information(node_id, flow_id).')

        if flow_json_file:
            try:
                flow_json = json.loads(flow_json_file)
                self.flow_obj.get_flow_list_ab(flow_json)
            except Exception as e:
                raise AssertionError('Type error, flow_json must be JSON(For nodered request type not UI type)')
        else:
            try:
                self.flow_obj.get_flow_list()
            except Exception as e:
                raise AssertionError('Request to NodeRed has porblem.')

        # get the node information in current_node_obj
        self.flow_obj.get_node_item(self.flow_obj.current_node_id)

        try:
            data = json.loads(REQUEST)['body']['data']
            self.data = DataFrame.from_dict(data)
        except Exception as e:
            raise AssertionError('Request contains no key named "data", or cannot transform to dataframe.')

    def get_param(self, key):
        """
        Get parameter from the key name, and it should be set from set_param.

        :param str key: The parameter key set from method set_param
        :return: Speicfic type depends on set_param. The value of the key name.
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
                obj_value = list(obj_value)
            else:
                _logger.warning('Parameter has no specific type.')
                obj_value = str(obj_value)
        except Exception as e:
            raise AssertionError('The value has problem when transfrom type.')

        if obj_value:
            return obj_value
        else:
            return None

    def get_data(self):
        """
        Transform REQUEST data to DataFrame type.

        :return: DataFrame type. Data from REQUEST and rename column name.
        """
        if self.data is not DataFrame.empty:
            return self.data.rename(columns=self.get_column())
        else:
            return DataFrame.empty

    def get_column(self):
        """
        Get the column mapping list.

        :return: The value is the column name would use in the AFS API, and the key is the mapping column name.
        :rtype: dict
        """
        return {self.flow_obj.current_node_obj[column_name]: column_name
                for column_name in self.flow_obj.current_node_obj
                if column_name in self.column}

    def next_node(self, data=None, debug=False):
        """
        Send data to next node according to flow.

        :param data: DataFrame type.
        :param bool debug: If debug is True, method will return response message from the next node.
        :return: Response JSON
        :rtype: dict
        """
        if data:
            if isinstance(data, DataFrame):
                column_reverse_mapping = {v: k for k, v in self.get_column().items()}
                data = data.rename(columns=column_reverse_mapping)
                data = dict(data=data.to_dict())
                return self.flow_obj.exe_next_node(data, debug=debug)
            else:
                raise AssertionError('Type error, data must be DataFrame type')

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
            raise AssertionError('Type not found.')
        else:
            # check default type
            if default:
                if not isinstance(default, self.type_list[type]):
                    raise AssertionError('Default value is not the specific type.')

        # check required value
        if not isinstance(required, bool):
            raise AssertionError('required is true/false.')

        # check if the name is the same, raise error
        if key in self.variable_name:
            raise AssertionError('It has already the same name of the parameter.')
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
            raise AssertionError('It has already the same column name.')
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
            raise AssertionError('Type Error enable  is bool type')

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
        smry = {}
        smry['features'] = self.features
        smry['param'] = self.param
        smry['column'] = self.column
        print(json.dumps(smry))
