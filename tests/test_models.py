
import pytest
import os
# from afs import models
# from dotenv import Dotenv
# dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env")) # Of course, replace by your correct path
# os.environ.update(dotenv)

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


def test_1(test):
    print(test)

def test_2(test):
    print(test)

def test_upload_model(models_resource, conf_resource, tmpdir):
    p=tmpdir.mkdir('data').join(conf_resource['model_name'])
    p.write('this is a model.')
    print(p)
    models_resource.upload_model(p, accuracy=.123, loss=.123)

def test_download_model(models_resource, conf_resource, tmpdir):
        p=tmpdir.mkdir('data')
        models_path=os.path.join(p, conf_resource['model_name'])
        models_resource.download_model(models_path, model_name=conf_resource['model_name'])
        with open(models_path) as f:
            content = f.read()
        assert 'this is a model.' == content

# class TestModels:
#     def models():
#         self.model_path = config['TestModels']['model_path']
#         self.model_name = config['TestModels']['model_name']
#
#         self.cli = models()
#
#     @pytest.fixture
#     def test_upload_model(self):
#         with open(self.model_path, 'w') as f:
#             f.write('this is a model.')
#         self.cli.upload_model(self.model_path, accuracy=.123, loss=.123)
#         os.remove('./data/test_model.h5')
#
#     @pytest.fixture
#     def test_download_model(self):
#         self.cli.download_model(self.model_path, model_name=self.model_name)
#         with open(self.model_path) as f:
#             content = f.read()
#         assert 'this is a model.' == content
#         os.remove('./data/test_model.h5')