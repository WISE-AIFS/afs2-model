import pytest

@pytest.fixture(scope='function')
def utils_resource():
    from afs import utils
    yield utils

def test_urljoin(mock_api_v2_resource, utils_resource):
    url = utils_resource.urljoin(mock_api_v2_resource.target_endpoint, 'instance_id', mock_api_v2_resource.instance_id, 'model_respositories', '123', extra_paths={})
    assert url == '{0}instance_id/{1}/model_respositories/123'.format(mock_api_v2_resource.target_endpoint, mock_api_v2_resource.instance_id)

def test_urljoin_extra_paths(mock_api_v2_resource, utils_resource):
    url = utils_resource.urljoin(mock_api_v2_resource.target_endpoint, 'instance_id', mock_api_v2_resource.instance_id, 'model_respositories', extra_paths=['123', 'upload'])
    assert url == '{0}instance_id/{1}/model_respositories/123/upload'.format(mock_api_v2_resource.target_endpoint, mock_api_v2_resource.instance_id)
