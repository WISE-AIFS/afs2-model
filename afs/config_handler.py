import json
from pandas import DataFrame
import pandas
from afs.flow import flow
import logging

_logger = logging.getLogger(__name__)

class config_handler(object):
    def __init__(self):
        self.param = []
        self.column = []

    def set_kernel_gateway(self, REQUEST, flow_json_file=None):

        self.flow_obj = flow()

        try:
            headers = json.loads(REQUEST)['headers']
            flow_info = {}
            flow_info['node_id'] = headers['node_id']
            flow_info['flow_id'] = headers['flow_id']
            flow_info['host_url'] = headers['host_url']
            self.flow_obj.set_flow_config(flow_info)
        except Exception as e:
            raise AssertionError('REQUEST must be json format, or headers contains not enough information')

        try:
            if flow_json_file:
                with open(flow_json_file) as f:
                    flow_json = f.read()
                flow_json = json.loads(flow_json)
                self.flow_obj.get_flow_list_ab(flow_json)
            else:
                self.flow_obj.get_flow_list()
        except Exception as e:
            raise AssertionError('Type error, flow_json must be JSON')

        self.flow_obj.get_node_item(self.flow_obj.current_node_id)

        try:
            data = json.loads(REQUEST)['body']
            self.data = DataFrame.from_dict(data)
        except Exception as e:
            raise AssertionError('Request contains no key named "data", or cannot transform to dataframe.')


    def get_param(self, key):
        obj_value = self.flow_obj.current_node_obj[key]
        obj_para = [x for x in self.param if x['name'] in key][0]
        if obj_para['type'] in 'integer':
            obj_value = int(obj_value)
        elif obj_para['type'] in 'string':
            obj_value = str(obj_value)
        elif obj_para['type'] in 'float':
            obj_value = float(obj_value)
        else:
            _logger.warning('Type has no specific type.')
            obj_value = str(obj_value)

        if obj_value:
            return obj_value
        else:
            return None

    def get_data(self, request_body):
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
        if self.data:
            return self.data
        else:
            return None

    def next_node(self,data, debug=False):
        if isinstance(data, DataFrame):
            data = dict(data=data.to_dict())
            return self.flow_obj.exe_next_node(data, debug)
        else:
            raise AssertionError('Type error, data must be Dataframe')

    def set_param(self, key, type='string', required=False ,default=None):
        param = {}
        param['name'] = key
        param['type'] = type
        param['required'] = required
        param['default'] = default

        # check if the name is the same, raise error

        self.param.append(param)
        pass

    def set_column(self, column_name):
        self.column.append(column_name)
        pass

    def summary(self):
        # print('AFS module information')
        smry = {}
        smry['param'] = self.param
        smry['column'] = self.column
        print(json.dumps(smry))
        pass




