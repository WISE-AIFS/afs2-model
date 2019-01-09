import pytest


def test_urljoin(mock_api_v2_resource, utils_resource):
    url = utils_resource.urljoin('http://afs.org.tw', 'instance_id', '1234-4567-7890', 'model_respositories', '123', extra_paths={})
    assert url == 'http://afs.org.tw/instance_id/1234-4567-7890/model_respositories/123'

def test_urljoin_extra_paths(mock_api_v2_resource, utils_resource):
    url = utils_resource.urljoin('http://afs.org.tw', 'instance_id', '1234-4567-7890', 'model_respositories', extra_paths=['123', 'upload'])
    assert url == 'http://afs.org.tw/instance_id/1234-4567-7890/model_respositories/123/upload'

