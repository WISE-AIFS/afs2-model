
from afs import config_handler
import json
import unittest
import configparser


class TestConfigHandler(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.flow_json_file=config['config_handler']['flow_json_file']
        with open(config['config_handler']['config_handler_request']) as f:
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

    def test_get_data(self):
        cfg = config_handler()
        cfg.set_param('b', type='integer', required=True, default=10)
        cfg.set_column('a')
        cfg.summary()

        cfg.set_kernel_gateway(self.REQUEST, flow_json_file=self.flow_json_file)
        a = cfg.get_data()
        print(a)
