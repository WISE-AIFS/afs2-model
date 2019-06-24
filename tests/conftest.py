import os, pytest
from tests.mock_requests import MockResponse
from dotenv import load_dotenv


load_dotenv()

@pytest.fixture(scope="session")
def client_session():
    from afs.client import EIPaaSAFSSession

    yield EIPaaSAFSSession()
