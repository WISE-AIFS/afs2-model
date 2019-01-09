import uuid, os, pytest
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

@pytest.fixture()
def test():
    return uuid.uuid4()

@pytest.fixture(scope='session')
def data_dir():
    yield os.path.join(os.path.dirname(__file__), 'data')

@pytest.fixture(scope='class')
def models_resource():
    from afs import models
    afs_models=models()
    yield afs_models

@pytest.fixture(scope='class')
def services_resource():
    from afs import services
    afs_services=services()
    yield afs_services

@pytest.fixture(scope='function')
def config_handler_resource():
    from afs import config_handler
    afs_config_handler = config_handler()
    yield afs_config_handler

@pytest.fixture(scope='class')
def conf_resource():
    conf={ "model_name":"test_model.h5"}
    return conf

@pytest.fixture(scope='session')
def client_session():
    from afs.client import EIPaaSAFSSession
    yield EIPaaSAFSSession()

@pytest.fixture(scope='function')
def mock_api_v2_resource(mocker):
    from afs.get_env import AfsEnv
    mocker.patch.object(AfsEnv, '_get_api_version', return_value='v2')
    yield AfsEnv()

@pytest.fixture(scope='function')
def mock_models(mocker):
    from afs import models
    yield models()

@pytest.fixture()
def model_name(test):
    test_model = 'test_model.h5'
    if os.path.exists(test_model):
        os.remove(test_model)

    with open(test_model, 'w') as f:
        f.write(str(test))

    yield test_model

    os.remove(test_model)