import json
import os
from uuid import uuid4

import pytest
from dotenv import load_dotenv

from .mock_response import MockResponse


@pytest.fixture(scope='session')
def v2_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env2")
    load_dotenv(dotenv_path=env_path)


@pytest.fixture()
def mock_api_v2_resource(mocker):
    import requests
    mocker.patch.dict(os.environ, {
        'afs_url': 'http://afs.org.tw',
        'instance_id': str(uuid4()),
        'auth_code': '1234',
        'version': '2.0.2'}
    )

    mock_response = {
        'API_version': 'v2',
        'AFS_version': '>=2.0.0'
    }
    mock_response = MockResponse(
        text=json.dumps(mock_response), status_code=200)

    mocker.patch.object(requests,
        'get',
        return_value=mock_response
    )
