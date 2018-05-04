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

    def set_flow(self, flow_json, node_info):
        self.flow_obj = flow()
        self.flow_obj.set_flow_config(node_info)
        self.flow_obj.get_flow_list_ab(flow_json)
        self.flow_obj.get_node_item(self.flow_obj.current_node_id)

    def get_param(self, key):
        obj = self.flow_obj.current_node_obj[key]
        if obj:
            return obj
        else:
            return None

    def next_node(self,data):
        self.flow_obj.exe_next_node(data)

    def set_param(self, key, type='string', required=False ,default=None):
        param = {}
        param['name'] = key
        param['tpye'] = type
        param['required'] = required
        param['default'] = default
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

    cfg = config_handler()
    cfg.set_param('b', type='integer', required=True, default=10)
    cfg.set_column('value')
    cfg.summary()

    cfg.set_flow(flow_json, req_body)
    b = cfg.get_param('b')
    a = DataFrame.from_dict(req_body['data'])
    result = a + int(b)
    df_dict = dict(data=result.to_dict())
    cfg.next_node(df_dict)



