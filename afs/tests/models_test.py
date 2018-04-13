
from afs import models
import unittest
import os

class TestModels(unittest.TestCase):
    def setUp(self):
        self.cli = models('https://portal-afs-develop.iii-cflab.com', 'f82c41f3-c6bb-478a-9c1d-670dcd3ab41c',
                    'PBh4wB6m1hPwB4C2C7jGXg')
        self.model_path = '.\\data\\test_model.h5'
        self.model_name = 'test_model.h5'

    def test_models(self):
        cli = models('host', '12345678-1234-1234-1234-123456789012',
               'abcdefghijklmnopqrstuv')
        self.assertEqual('host/v1/', cli.target_endpoint)
        self.assertEqual('12345678-1234-1234-1234-123456789012', cli.instance_id)
        self.assertEqual('abcdefghijklmnopqrstuv', cli.auth_code)
        print('test models (1/1)')

    def test_download_model(self):
        self.cli.download_model(self.model_path, model_name=self.model_name)
        with open(self.model_path) as f:
            content = f.read()
        self.assertEqual('this is a model.', content)
        os.remove('./data/test_model.h5')
        print('test download model (1/1)')

    def test_upload_model(self):
        with open(self.model_path, 'w') as f:
            f.write('this is a model.')
        self.cli.upload_model(self.model_path, accuracy=.123, loss=.123)
        os.remove('./data/test_model.h5')
        print('test upload model (1/1)')

if __name__ == '__main__':
    cli = TestModels()
    cli.setUp()
    cli.test_models()
    cli.test_upload_model()
    cli.test_download_model()

