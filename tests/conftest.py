import os, pytest
from tests.mock_requests import MockResponse
from dotenv import load_dotenv

@pytest.fixture(scope="session")
def client_session():
    from afs.client import EIPaaSAFSSession

    yield EIPaaSAFSSession()


@pytest.fixture(scope="session")
def test_env():
    load_dotenv()


@pytest.fixture(scope="session")
def test_param_token():
    load_dotenv()
    
    yield {
        "afs_url": os.getenv("afs_url"),
        "instance_id": os.getenv("instance_id"),
        "token": os.getenv("token"),
    }
