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

    def set_flow(self, obj):
        self.flow_obj = flow()
        self.flow_obj.get_flow_list_ab(obj)
        print(self.flow_obj.flow_list)
        # self.flow_obj.set_flow_config(obj)

    def get_node_item(self, select_node_id):
        obj = self.flow_obj.get_node_item(select_node_id)
        for par in self.param:
            par
        return obj

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
    cfg = config_handler()
    cfg.set_param('b', type='integer', required=True, default=10)
    cfg.set_column('value')
    cfg.summary()

    with open('tests/add_node.json') as f:
        flow_json = f.read()
    flow_json = json.loads(flow_json)
    cfg.set_flow(flow_json)
    print(cfg.get_node_item('ada49faf.e05cf'))
