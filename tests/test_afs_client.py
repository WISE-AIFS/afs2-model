import os

from afs import AFSClient
from afs.clients.base import APISession
from afs.clients.instances import InstancesClient
from afs.clients.sso import SSOClient


def test_afs_client():
    afs_client = AFSClient(
        api_endpoint=os.getenv('TEST_AFS_API_SERVER'),
        username=os.getenv('TEST_USERNAME'),
        password=os.getenv('TEST_PASSWORD')
    )

    session = getattr(afs_client, 'session')
    assert isinstance(session, APISession)

    api_endpoint = getattr(afs_client, 'api_endpoint')
    assert isinstance(api_endpoint, str)
    assert api_endpoint == os.getenv('TEST_AFS_API_SERVER')

    # Check SSO client
    sso_client = getattr(afs_client, 'sso')
    assert isinstance(sso_client, SSOClient)

    # Check token and this token is set at session's headers
    token = getattr(afs_client, 'token')
    assert isinstance(token, str)
    assert 'Bearer {}'.format(token) == session.headers.get('Authorization')

    # Check instance client
    instances_client = getattr(afs_client, 'instances')
    assert isinstance(instances_client, InstancesClient)


def test_get_api_info(afs_client):
    api_info = afs_client.get_api_info()
    assert isinstance(api_info, dict)
    assert 'API_version' in api_info
    assert api_info['API_version'] == 'v2'
    assert 'AFS_version' in api_info

def test_get_api_version(afs_client):
    api_version = afs_client.get_api_version()
    assert isinstance(api_version, str)
    assert api_version == 'v2'
