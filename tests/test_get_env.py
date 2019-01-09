from tests.mock_requests import MockResponse

def test_info_v2_check(mock_api_v2_resource, utils_resource, mocker):
    import afs
    mocker.patch('afs.utils.urljoin')
    from afs.get_env import AfsEnv
    AfsEnv()
    afs.utils.urljoin.assert_called_once_with('http://afs.org.tw/', extra_paths={})

def test_info_v1_check(mocker, mock_api_v1_resource):
    import afs
    import os
    mocker.patch('afs.utils.urljoin')
    from afs.get_env import AfsEnv
    AfsEnv()
    afs.utils.urljoin.assert_called_once_with('http://afs.org.tw/' , 'info', extra_paths={})