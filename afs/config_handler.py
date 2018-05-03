import json
from pandas import DataFrame
import pandas


class config(object):
    def __init__(self):
        self.input = {}
        self.output = {}
        self.column_mapping = []





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


    def set_input(self, key, type='string', required=False ,default=None):
        self.input[key] = {}
        self.input[key]['tpye'] = type
        self.input[key]['required'] = required
        self.input[key]['default'] = default
        pass

    def set_column_mapping(self, column_name):
        self.column_mapping.append(column_name)
        pass

    def summary(self):
        smry = {}
        smry['input'] = self.input
        smry['output'] = self.output
        smry['column_mapping'] = self.column_mapping
        print(json.dumps(smry))
        pass

    def set_output(self):
        pass

    def _read_flow(self, flow_json):
        print(flow_json)
        pass



if __name__ == '__main__':
    cfg = config()
    cfg.set_input('b', type='integer', required=True, default=10)
    cfg.set_column_mapping('value')
    cfg.summary()

    with open('tests/add_node.json') as f:
        flow_json = f.read()
    flow_json = json.loads(flow_json)
    cfg._read_flow(flow_json)