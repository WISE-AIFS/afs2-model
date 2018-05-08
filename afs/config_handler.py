import json
from pandas import DataFrame
import pandas
from afs import flow
import logging

_logger = logging.getLogger(__name__)

class config_handler(object):
    def __init__(self):
        self.param = []
        self.column = []

    def set_flow(self, flow_json, request_body):
        try:
            request_body = json.loads(request_body)
        except Exception as e:
            raise AssertionError('Type error, request_body must be JSON')

        self.flow_obj = flow()
        self.flow_obj.set_flow_config(request_body)
        self.flow_obj.get_flow_list_ab(flow_json)
        self.flow_obj.get_node_item(self.flow_obj.current_node_id)

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
                return DataFrame.from_dict(request_body['data'])
            else:
                raise AssertionError('Data is not existed in request_body')
        except Exception as e:
            raise AssertionError('Type error, request_body must be JSON')

    def next_node(self,data):
        if isinstance(data, DataFrame):
            data = dict(data=data.to_dict())
            self.flow_obj.exe_next_node(data)
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


if __name__ == '__main__':
    # node-red config and request body
    with open('tests/add_node.json') as f:
        flow_json = f.read()
    flow_json = json.loads(flow_json)
    req_body = {'data': {'value': {'0': 21}}, 'node_id': 'ada49faf.e05cf'}
    req_body = json.dumps(req_body)

    cfg = config_handler()
    cfg.set_param('b', type='integer', required=True, default=10)
    cfg.set_column('value')
    cfg.summary()

    cfg.set_flow(flow_json, req_body)
    b = cfg.get_param('b')
    a = cfg.get_data(req_body)
    result = a + b
    cfg.next_node(result)



