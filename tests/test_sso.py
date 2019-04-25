import os

import pytest


@pytest.fixture(scope="module")
def sso_client(afs_client):
    yield afs_client.sso


def test_get_sso_token(sso_client):

    username = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PASSWORD")

    token = sso_client.get_sso_token(username=username, password=password)

    assert isinstance(token, str)


def test_refresh_sso_token(sso_client):
    token = sso_client._session.token
    new_token = sso_client.refresh_sso_token(token)

    assert token != new_token
