
from afs import config_handler
import json
import unittest
import configparser


class TestModels(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.flow_json_file='./data/flow_json.json'
        with open('./data/config_handler_request.json') as f:
            self.REQUEST = f.read()

    def test_adder(self):
        cfg = config_handler()
        cfg.set_param('b', type='integer', required=True, default=10)
        cfg.set_column('a')
        cfg.summary()

        cfg.set_kernel_gateway(self.REQUEST, flow_json_file=self.flow_json_file)
        b = cfg.get_param('b')
        a = cfg.get_data()
        result = a + b
        ret = cfg.next_node(result, debug=True)
        print(json.dumps(ret))