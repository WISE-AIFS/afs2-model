
import pytest
import os
from afs import models
from dotenv import Dotenv
dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env")) # Of course, replace by your correct path
os.environ.update(dotenv)

# class  TestSample :
#    @pytest.fixture()
#    def  count (self) :
#        print( 'init count' )
#        return  10
#    def  test_answer (self, count) :
#        print( 'get count %s' % count)
#        assert count == 10
#    def test_env(self):
#        print(os.getenv('afs_url'))
#        assert 1 == 1


class TestModels:
    def setUp(self):
        self.model_path = config['TestModels']['model_path']
        self.model_name = config['TestModels']['model_name']

        self.cli = models()

    @pytest.fixture
    def test_upload_model(self):
        with open(self.model_path, 'w') as f:
            f.write('this is a model.')
        self.cli.upload_model(self.model_path, accuracy=.123, loss=.123)
        os.remove('./data/test_model.h5')

    def test_download_model(self):
        self.cli.download_model(self.model_path, model_name=self.model_name)
        with open(self.model_path) as f:
            content = f.read()
        assert 'this is a model.' == content
        os.remove('./data/test_model.h5')