import json
from pandas import DataFrame
import pandas
from afs.flow import flow
import logging

_logger = logging.getLogger(__name__)

class config_handler(object):
    def __init__(self):
        """
Config handler is the class which handle AFS flow framework. User can use function fetch parameters, or send data to next node.
        """
        self.param = []
        self.param_name = []
        self.column = []
        self.data = DataFrame.empty

    def set_kernel_gateway(self, REQUEST, flow_json_file=None):

        """
For Jupyter kernel gateway API, REQUEST is pure request given by kernel gateway. Reference REQUEST: http://jupyter-kernel-gateway.readthedocs.io/en/latest/http-mode.html
        :param REQUEST: Jupyter kernel gateway request.
        :param flow_json_file:
        """
        self.flow_obj = flow()

        try:
            headers = json.loads(REQUEST)['headers']
            flow_info = {}
            flow_info['node_id'] = headers['Node_id']
            flow_info['flow_id'] = headers['Flow_id']
            flow_info['host_url'] = headers['Host_url']
            self.flow_obj.set_flow_config(flow_info)
        except Exception as e:
            raise AssertionError('REQUEST must be json format, or headers contains not enough information')

        if flow_json_file:
            try:
                with open(flow_json_file) as f:
                    flow_json = f.read()
                flow_json = json.loads(flow_json)
                self.flow_obj.get_flow_list_ab(flow_json)
            except Exception as e:
                raise AssertionError('Type error, flow_json must be JSON')
        else:
            try:
                self.flow_obj.get_flow_list()
            except Exception as e:
                raise AssertionError('Request to NodeRed has porblem.')


        self.flow_obj.get_node_item(self.flow_obj.current_node_id)

        try:
            data = json.loads(REQUEST)['body']['data']
            self.data = DataFrame.from_dict(data)
        except Exception as e:
            raise AssertionError('Request contains no key named "data", or cannot transform to dataframe.')

    def get_param(self, key):
        """
Get parameter from key name, and it should be set from set_param.
        :param key: the parameter key set from method set_param
        :return: the value of the key
        """
        obj_value = self.flow_obj.current_node_obj[key]
        obj_para = [x for x in self.param if x['name'] in key][0]
        if obj_para['type'] in 'integer':
            obj_value = int(obj_value)
        elif obj_para['type'] in 'string':
            obj_value = str(obj_value)
        elif obj_para['type'] in 'float':
            obj_value = float(obj_value)
        else:
            _logger.warning('Param has no specific type.')
            obj_value = str(obj_value)

        if obj_value:
            return obj_value
        else:
            return None

    def get_data(self, request_body):
        """

        :param request_body:
        :return: DataFrame type from REQUEST
        """
        try:
            request_body = json.loads(request_body)
            if request_body['data']:
                self.data = DataFrame.from_dict(request_body['data'])
                return self.data
            else:
                raise AssertionError('Data is not existed in request_body')
        except Exception as e:
            raise AssertionError('Type error, request_body must be JSON')

    def get_data(self):
        """
Transform REQUEST data to DataFrame type.
        :return: DataFrame type from REQUEST
        """
        if self.data is not DataFrame.empty:
            return self.data
        else:
            return DataFrame.empty

    def next_node(self,data, debug=False):
        """
Send data to next node according to flow.
        :param data: DataFrame type.
        :param debug: if debug is True, method will return response message from next node.
        :return:
        """
        if isinstance(data, DataFrame):
            data = dict(data=data.to_dict())
            return self.flow_obj.exe_next_node(data, debug)
        else:
            raise AssertionError('Type error, data must be Dataframe')

    def set_param(self, key, type='string', required=False ,default=None):
        """
Set API parameter will be used in the API.
        :param key: the key name for this parameter
        :param type: the type is paramter, integer, string or float.
        :param required: the parameter is required or not
        :param default: the parameter is given in default
        """

        param = {}
        param['name'] = key
        param['type'] = type
        param['required'] = required
        param['default'] = default

        # check if the name is the same, raise error
        if key in self.param_name:
            raise AssertionError('It has already the same name parameter.')
        else:
            self.param_name.append(key)
            self.param.append(param)
        pass

    def set_column(self, column_name):
        """
The column will be used in this API.
        :param column_name:
        """
        self.column.append(column_name)
        pass

    def summary(self):
        """
Summary what parameters and column the API need.This method should be called by the last line in the 2nd cell.
        """
        smry = {}
        smry['param'] = self.param
        smry['column'] = self.column
        print(json.dumps(smry))
        pass




