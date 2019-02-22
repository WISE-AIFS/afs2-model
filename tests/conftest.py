import os

import pytest

from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)


@pytest.fixture(scope="session")
def afs_client():
    from afs import AFSClient

    afs_client = AFSClient(
        api_endpoint=os.getenv("TEST_AFS_API_SERVER"),
        username=os.getenv("TEST_USERNAME"),
        password=os.getenv("TEST_PASSWORD"),
    )

    yield afs_client


@pytest.fixture(scope="session")
def instance_id():
    yield os.getenv("TEST_SERVICE_INSTANCE")


@pytest.fixture(scope="session")
def instance(afs_client, instance_id):
    yield afs_client.instances(instance_id)
