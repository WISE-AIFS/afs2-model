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
        self.flow_obj.set_flow_config(obj)

        self.flow_obj.get_node_item()

    def next_node(self,data):
        self.flow_obj.exe_next_node(data)



        # if not isinstance(REQUEST, json):
        #     AssertionError('REQUEST type is not json format')
        #
        # param = {}
        # headers = {}
        #
        # self.request_body = json.loads(REQUEST)
        # self.body = self.request_body['body']
        # self.data = self.body['data']
        # self.headers = self.request_body['headers']
        #
        # if 'flow_id' in headers and 'node_id' in headers and 'host_url' in headers:
        #     pass
        # else:
        #     pass
        #
        # required = [tag for tag in input_config['param'] if 'default' not in input_config['param'][tag]]
        # optional = [tag for tag in input_config['param'] if 'default' in input_config['param'][tag]]
        #
        # for tag in required:
        #     if tag in self.body:
        #         param[tag] = self.body[tag]
        #     else:
        #         AssertionError('Some required tags are lost')
        #
        # for tag in optional:
        #     if tag in self.body:
        #         param[tag] = self.body['tag']
        #     else:
        #         param[tag] = input_config['param'][tag]['default']
        #
        # dataframe = DataFrame.from_dict(data)


    def set_param(self, key, type='string', required=False ,default=None):
        param = {}
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
        # smry['output'] = self.output
        smry['column'] = self.column
        print(json.dumps(smry))
        pass

    def set_output(self):

        pass

    def _read_flow(self, flow_json):
        print(flow_json)
        pass



if __name__ == '__main__':
    cfg = config_handler()
    cfg.set_param('b', type='integer', required=True, default=10)
    cfg.set_column('value')
    cfg.summary()

    with open('tests/add_node.json') as f:
        flow_json = f.read()
    flow_json = json.loads(flow_json)
    cfg._read_flow(flow_json)