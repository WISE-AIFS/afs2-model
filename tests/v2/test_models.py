import pytest
from tests.mock_requests import MockResponse
import os

@pytest.fixture(scope='function')
def mock_api_v2_resource(mocker):
    from afs.get_env import AfsEnv
    mocker.patch.object(AfsEnv, '_get_api_version', return_value='v2')
    yield AfsEnv()

@pytest.fixture(scope='function')
def mock_models(mocker):
    from afs import models
    yield models()

@pytest.fixture(scope='function')
def model_name(test):
    test_model = 'test_model.h5'
    if os.path.exists(test_model):
        os.remove(test_model)

    with open(test_model, 'w') as f:
        f.write(str(test))

    yield test_model

    os.remove(test_model)

# v2 API unit_test
def test_upload_model_v2(mocker, test, mock_api_v2_resource, mock_models, model_name):
    with open(model_name, 'w') as f:
        f.write(str(test))
    mocker.patch.object(mock_models, 'switch_repo', return_value=None)
    mocker.patch.object(mock_models, 'create_model_repo', return_value='123')
    mocker.patch.object(mock_models, '_put', return_value=MockResponse(status_code=200, text="""
    {
      "uuid": "c2714f44-fab9-4bde-afc9-7b3ab40cd431",
      "name": "test_model.h5",
      "created_at": "2018-08-20 09:16:18",
      "models": [
        "b5e8399d-3a95-42a5-88f5-79b8cdeb4045"
      ]
    }"""))
    assert mock_models.upload_model(model_name, accuracy=.123, loss=.123) == True


# v2 API unit_test
def test_create_model_repo_v2(mocker, mock_api_v2_resource, mock_models, model_name):
    mocker.patch.object(mock_models, '_create', return_value=MockResponse(text="""
    {
        "uuid": "c2714f44-fab9-4bde-afc9-7b3ab40cd431",
        "name": "test_model.h5",
        "created_at": "2018-08-20 09:16:18",
        "models": []
    }""", status_code=200))
    assert mock_models.create_model_repo(model_name) == "c2714f44-fab9-4bde-afc9-7b3ab40cd431"

# v2 API unit_test
def test_switch_repo_v2(mocker, mock_api_v2_resource, mock_models, model_name):
    mocker.patch.object(mock_models, '_get', return_value=MockResponse(text="""
    [{
      "uuid": "c2714f44-fab9-4bde-afc9-7b3ab40cd431",
      "name": "test_model.h5",
      "created_at": "2018-08-20 09:16:18",
      "models": [
        "b5e8399d-3a95-42a5-88f5-79b8cdeb4045"
      ]
    }]
      """, status_code=200)
    )
    assert mock_models.switch_repo(model_name) == "c2714f44-fab9-4bde-afc9-7b3ab40cd431"


@pytest.fixture(scope='function')
def utils_resource():
    from afs import utils
    yield utils

def test_urljoin(mock_api_v2_resource, utils_resource):
    url = utils_resource._urljoin(mock_api_v2_resource.target_endpoint, 'instance_id', mock_api_v2_resource.instance_id, 'model_respositories', '123', extra_paths={})
    assert url == '{0}instance_id/{1}/model_respositories/123'.format(mock_api_v2_resource.target_endpoint, mock_api_v2_resource.instance_id)

def test_urljoin_extra_paths(mock_api_v2_resource, utils_resource):
    url = utils_resource._urljoin(mock_api_v2_resource.target_endpoint, 'instance_id', mock_api_v2_resource.instance_id, 'model_respositories', extra_paths=['123', 'upload'])
    assert url == '{0}instance_id/{1}/model_respositories/123/upload'.format(mock_api_v2_resource.target_endpoint, mock_api_v2_resource.instance_id)
