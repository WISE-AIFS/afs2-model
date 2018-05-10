from afs import models
import unittest
import os
import configparser

class TestModels(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.target_endpoint = config['TestModels']['target_endpoint']
        self.instance_id = config['TestModels']['instance_id']
        self.auth_code = config['TestModels']['auth_code']
        self.model_path = config['TestModels']['model_path']
        self.model_name = config['TestModels']['model_name']

        self.cli = models(target_endpoint=self.target_endpoint, instance_id=self.instance_id,
                    auth_code=self.auth_code)

    def test_init(self):

        self.assertEqual(self.target_endpoint + '/host/v1/', self.cli.target_endpoint)
        self.assertEqual(self.instance_id, self.cli.instance_id)
        self.assertEqual(self.auth_code, self.cli.auth_code)

    def test_download_model(self):
        self.cli.download_model(self.model_path, model_name=self.model_name)
        with open(self.model_path) as f:
            content = f.read()
        self.assertEqual('this is a model.', content)
        os.remove('./data/test_model.h5')

    def test_upload_model(self):
        with open(self.model_path, 'w') as f:
            f.write('this is a model.')
        self.cli.upload_model(self.model_path, accuracy=.123, loss=.123)
        os.remove('./data/test_model.h5')

