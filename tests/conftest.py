import os, pytest
from tests.mock_requests import MockResponse
from dotenv import load_dotenv


@pytest.fixture(scope='session')
def v1_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)


@pytest.fixture(scope='session')
def v2_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env2")
    load_dotenv(dotenv_path=env_path)


@pytest.fixture(scope='class')
def models_resource():
    from afs import models
    afs_models=models()
    yield afs_models


@pytest.fixture(scope='session')
def client_session():
    from afs.client import EIPaaSAFSSession
    yield EIPaaSAFSSession()


@pytest.fixture(scope='module')
def utils_resource():
    from afs import utils
    yield utils


@pytest.fixture()
def mock_api_v2_resource(mocker):
    import requests
    mocker.patch.dict(os.environ, {
        'afs_url': 'http://afs.org.tw',
        'instance_id': '1234-4567-7890',
        'auth_code': '1234',
        'version': '2.0.2'}
    )
    mocker.patch.object(requests,
        'get',
        return_value=MockResponse(text="""{"API_version":"v2", "AFS_version":"2.1.1.dev0"}""",
                                  status_code=200)
    )


@pytest.fixture()
def mock_api_v1_resource(mocker):
    import requests
    mocker.patch.dict(os.environ, {
        'afs_url': 'http://afs.org.tw',
        'instance_id': '1234-4567-7890',
        'auth_code': '1234',
        'version': '1.2.29'}
    )
    mocker.patch.object(requests, 'get',
        return_value=MockResponse(text="""{"API_version":"v1", "AFS_version":"1.2.29"}""",
                                  status_code=200)
        )


@pytest.fixture()
def mock_api_v2_AFS_API_VERSION_resource(mocker):
    import requests
    mocker.patch.dict(os.environ, {
        'afs_url': 'http://afs.org.tw',
        'instance_id': '1234-4567-7890',
        'auth_code': '1234',
        'AFS_API_VERSION': '2.1.7'}
    )
    mocker.patch.object(requests, 'get',
        return_value=MockResponse(text="""{"API_version":"v2", "AFS_version":"2.1.7"}""",
                                  status_code=200)
        )
    from afs.get_env import AfsEnv
    yield AfsEnv()



