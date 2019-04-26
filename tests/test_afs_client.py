import os

from urllib.parse import urljoin

import pytest
import requests

from urllib3.exceptions import InsecureRequestWarning

from afs2_model import AFSClient
from afs2_model.clients.base import APISession
from afs2_model.clients.instances import InstancesClient
from afs2_model.clients.sso import SSOClient


@pytest.fixture()
def sso_token():
    sso_endpoint = os.getenv("TEST_AFS_API_SERVER").replace("api-afs", "portal-sso")
    resp = requests.post(
        urljoin(sso_endpoint, "/v2.0/auth/native"),
        json={
            "username": os.getenv("TEST_USERNAME"),
            "password": os.getenv("TEST_PASSWORD"),
        },
    )

    token = resp.json()["accessToken"]
    yield token


def test_afs_client():
    afs_client = AFSClient(
        api_endpoint=os.getenv("TEST_AFS_API_SERVER"),
        username=os.getenv("TEST_USERNAME"),
        password=os.getenv("TEST_PASSWORD"),
    )

    session = getattr(afs_client, "_session")
    assert isinstance(session, APISession)

    api_endpoint = getattr(afs_client, "api_endpoint")
    assert isinstance(api_endpoint, str)
    assert api_endpoint == os.getenv("TEST_AFS_API_SERVER")

    # Check SSO client
    sso_client = getattr(afs_client, "sso")
    assert isinstance(sso_client, SSOClient)

    # Check token and this token is set at session's headers
    token = getattr(afs_client._session, "token")
    assert isinstance(token, str)
    assert "Bearer {}".format(token) == session.headers.get("Authorization")

    # Check instance client
    instances_client = getattr(afs_client, "instances")
    assert isinstance(instances_client, InstancesClient)


def test_afs_client_with_sso_token(sso_token):
    afs_client = AFSClient(
        api_endpoint=os.getenv("TEST_AFS_API_SERVER"), token=sso_token
    )

    session = getattr(afs_client, "_session")
    assert isinstance(session, APISession)

    api_endpoint = getattr(afs_client, "api_endpoint")
    assert isinstance(api_endpoint, str)
    assert api_endpoint == os.getenv("TEST_AFS_API_SERVER")

    # Check SSO client
    sso_client = getattr(afs_client, "sso")
    assert isinstance(sso_client, SSOClient)

    # Check token and this token is set at session's headers
    token = getattr(afs_client._session, "token")
    assert isinstance(token, str)
    assert "Bearer {}".format(token) == session.headers.get("Authorization")

    # Check instance client
    instances_client = getattr(afs_client, "instances")
    assert isinstance(instances_client, InstancesClient)


def test_get_api_info(afs_client):
    api_info = afs_client.get_api_info()
    assert isinstance(api_info, dict)
    assert "API_version" in api_info
    assert api_info["API_version"] == "v2"
    assert "AFS_version" in api_info


def test_get_api_version(afs_client):
    api_version = afs_client.get_api_version()
    assert isinstance(api_version, str)
    assert api_version == "v2"


def test_ssl_ignore():
    with pytest.warns(InsecureRequestWarning):
        afs_client = AFSClient(
            api_endpoint=os.getenv("TEST_AFS_API_SERVER"),
            username=os.getenv("TEST_USERNAME"),
            password=os.getenv("TEST_PASSWORD"),
            ssl=False,
        )
