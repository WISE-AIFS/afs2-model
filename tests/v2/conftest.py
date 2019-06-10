import os, pytest, uuid
from tests.mock_requests import MockResponse
from dotenv import load_dotenv
from afs import models

load_dotenv()

@pytest.fixture(scope='session')
def model_file():
  with open('unit_test_model', 'w') as f:
      f.write('unit test')
  yield 

  os.remove('unit_test_model')
  if os.path.exists('delete_mr_and_model'):
      os.remove('delete_mr_and_model')


@pytest.fixture(scope='function')
def afs_models():
  my_models = models()
  yield my_models


@pytest.fixture(scope='function')
def model_repository(afs_models):
  yield afs_models.create_model_repo(model_repository_name='test_model_repository')


@pytest.fixture(scope='function')
def model(afs_models, model_repository, model_file):
  yield afs_models.upload_model(model_path='unit_test_model',
                            extra_evaluation={'extra_loss': 1.23},
                            model_repository_name='test_model_repository',
                            model_name='test_model')


@pytest.fixture(scope='function')
def delete_model_respository(afs_models):
  yield
  afs_models.delete_model_repository(model_repository_name='test_model_repository')


@pytest.fixture(scope='function')
def delete_mr_and_model(afs_models):
  yield 
  afs_models.delete_model(model_name='test_model', model_repository_name='test_model_repository')
  afs_models.delete_model_repository(model_repository_name='test_model_repository')


@pytest.fixture(scope='function')
def apm_node_env():
  os.environ['PAI_DATA_DIR'] = """{
      "type": "apm-firehose",
      "data": {
          "machineIdList": [3]
      }
  }"""
  yield
  del os.environ['PAI_DATA_DIR']
