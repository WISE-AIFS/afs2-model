import pytest

def test_init(mocker, afs_resource):
    import afs
    mocker.patch.object(afs, 'afs_portal_version', '1.3.0')
    assert afs_resource.afs_portal_version.startswith('1.3')

def test_env(mocker):
    from afs import get_env
    mocker.patch.object(get_env.AfsEnv, '_get_api_version', return_value='v2')
    env = get_env.AfsEnv()
    assert 'v2' in env.target_endpoint.split('/')
