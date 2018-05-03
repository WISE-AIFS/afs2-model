import json
from pandas import DataFrame
import pandas

input_config = {
    "param":{
         "frequency": {
             "type": "text",
             "default": 30
         },
         "password": {
             "type":"password"
         }
    },
    "column": [
         "AE_TEMPERATURE", "timestamp"
    ]
}

REQUEST = {
    "body": {
        "data": {
              "AE_TEMPERATURE": { '0': -0.95, '1': -0.951, '2': -0.951, '3': -0.952, '4': -0.952 },
              "channel": { '0': 'ch1', '1': 'ch1', '2': 'ch1', '3': 'ch1', '4': 'ch1' },
              "machine": { '0': None, '1': None, '2': None, '3': None, '4': None },
              "smartbox": { '0': 'box1', '1': 'box1', '2': 'box1', '3': 'box1', '4': 'box1' },
              "time":  { '0': '2018-03-22T08:32:17.666875Z',
                         '1': '2018-03-22T08:32:17.667125Z',
                         '2': '2018-03-22T08:32:17.667375Z',
                         '3': '2018-03-22T08:32:17.667625Z',
                         '4': '2018-03-22T08:32:17.667875Z' }
        },
        "password": "password"
    },
    "headers": {},
}
REQUEST = json.dumps(REQUEST)


class request_handler(object):
    def init(self, REQUEST, input_config):

        if not isinstance(REQUEST, json):
            AssertionError('REQUEST type is not json format')

        param = {}
        headers = {}

        self.request_body = json.loads(REQUEST)
        self.body = self.request_body['body']
        self.data = self.body['data']
        self.headers = self.request_body['headers']

        if 'flow_id' in headers and 'node_id' in headers and 'host_url' in headers:
            pass
        else:
            pass

        required = [tag for tag in input_config['param'] if 'default' not in input_config['param'][tag]]
        optional = [tag for tag in input_config['param'] if 'default' in input_config['param'][tag]]

        for tag in required:
            if tag in self.body:
                param[tag] = self.body[tag]
            else:
                AssertionError('Some required tags are lost')

        for tag in optional:
            if tag in self.body:
                param[tag] = self.body['tag']
            else:
                param[tag] = input_config['param'][tag]['default']

        dataframe = DataFrame.from_dict(self.data)

        return dataframe, param, headers

if __name__ == '__main__':
    # print(input_format(REQUEST,input_config))