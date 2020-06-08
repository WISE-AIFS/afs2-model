import os, pytest
from dotenv import load_dotenv
import requests
import json
import base64

@pytest.fixture(scope="session")
def test_env():
    load_dotenv()

    blobstore = json.loads(os.getenv('blobstore'))
    credentials = json.loads(os.getenv('blobstore'))['credentials']
    mapping = {
        "blob_endpoint": 'endpoint', 
        "blob_accessKey": "accessKey",
        "blob_secretKey": "secretKey"}
    for k, v in mapping.items():
        os.environ[k] = credentials[v]

    mapping = {
        'bucket_name': 'bucket_name',
        'blob_record_id': 'blob_record_id'
    }
    for k, v in mapping.items():
        os.environ[k] = blobstore[v]
        
    os.environ['blob_accessKey'] = str(base64.b64encode(bytes(os.environ['blob_accessKey'], 'utf-8')), 'utf-8')
    os.environ['blob_secretKey'] = str(base64.b64encode(bytes(os.environ['blob_secretKey'], 'utf-8')), 'utf-8')

@pytest.fixture(scope="session")
def test_param_token():
    load_dotenv()
    
    url = os.getenv('sso_endpoint') + '/v4.0/auth'
    payload = {
        "username": os.getenv("sso_username"),
        "password": os.getenv("sso_password")
    }
    resp = requests.post(url, json=payload ,verify=False)
    if resp.status_code == requests.codes.ok:
        token = 'Bearer ' + resp.cookies['EIToken']
    else:
        raise ConnectionError('SSO endpoint failed. status_code: {}, sso_endpoint: {}, username: {}'.format(
            resp.status_code,
            url, 
            os.getenv("sso_username")))

    yield {
        "afs_url": os.getenv("afs_url"),
        "instance_id": os.getenv("instance_id"),
        "token": token,
    }
