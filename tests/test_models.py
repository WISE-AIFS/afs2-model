import os
import pytest
import requests
import json


class response():
    def __init__(self, headers=None, body=None, status_code=None):
        self.headers = headers
        self.body = body
        self.status_code = status_code
    def json(self):
        return json.loads(self.body)


# v2 API unit_test
def test_upload_model_v2(mocker, test):
    name = 'test_model.h5'
    with open(name, 'w') as f:
        f.write(str(test))
    from afs import models
    from afs.get_env import AfsEnv
    mocker.patch.object(AfsEnv, '_get_api_version', return_value='v2')
    models_resource = models()
    mocker.patch.object(models, 'switch_repo', return_value=None)
    mocker.patch.object(models, 'create_model_repo', return_value='123')
    mocker.patch.object(models, '_put', return_value=response(status_code=200))
    assert models_resource.upload_model(name, accuracy=.123, loss=.123) == True


# v2 API unit_test
def test_create_model_repo_v2(mocker):
    from afs import models
    from afs.get_env import AfsEnv
    mocker.patch.object(AfsEnv, '_get_api_version', return_value='v2')
    models_resource = models()
    mocker.patch.object(models, '_create', return_value=response(body="""
    {
        "uuid": "c2714f44-fab9-4bde-afc9-7b3ab40cd431",
        "name": "test_create_model",
        "created_at": "2018-08-20 09:16:18",
        "models": [
            "b5e8399d-3a95-42a5-88f5-79b8cdeb4045"
        ]
    }""", status_code=200))
    assert models_resource.create_model_repo(name) == "c2714f44-fab9-4bde-afc9-7b3ab40cd431"

# v2 API unit_test
def test_switch_repo(mocker):
    name = 'test_create_model.h5'
    from afs import models
    from afs.get_env import AfsEnv
    mocker.patch.object(AfsEnv, '_get_api_version', return_value='v2')
    models_resource = models()
    mocker.patch.object(models, '_get', return_value=response(body="""
    [{
      "uuid": "c2714f44-fab9-4bde-afc9-7b3ab40cd431",
      "name": "test_create_model",
      "created_at": "2018-08-20 09:16:18",
      "models": [
        "b5e8399d-3a95-42a5-88f5-79b8cdeb4045"
      ]
      }]
      """, status_code=200)
    )
    assert models_resource.switch_repo(name) == "c2714f44-fab9-4bde-afc9-7b3ab40cd431"


# Positive test
def test_upload_model(models_resource, test):
    name = 'test_model.h5'
    with open(name, 'w') as f:
        f.write(str(test))
    models_resource.upload_model(name, accuracy=.123, loss=.123)
    if os.path.exists(name):
        os.remove(name)


# Positive test
def test_download_model(models_resource, test):
    name = 'test_model.h5'
    try:
        models_resource.download_model(name, model_name=name)
        assert os.path.exists(name)

        with open(name, 'r') as f:
            content = f.read()
        print(content)
        assert str(test) == str(content)
    except Exception as e:
        print(e)
    finally:
        if os.path.exists(name):
            os.remove(name)


# Positive test
def test_get_latest_model_info(models_resource):
    name = 'test_model.h5'
    model_info = models_resource.get_latest_model_info(name)
    assert model_info['evaluation_result']['accuracy'] == .123
    assert model_info['evaluation_result']['loss'] == .123


# Negative test
def test_model_accuracy(models_resource, test):
    name = 'test_model.h5'
    with open(name, 'w') as f:
        f.write(str(test))
    with pytest.raises(Exception):
        pytest.raises(
            models_resource.upload_model(name, accuracy=1.23, loss=.123))
    if os.path.exists(name):
        os.remove(name)


# Negative test
def test_model_naming_length(models_resource, test):
    a = ['a' for i in range(100)]
    name = '.'.join(a)
    with open(name, 'w') as f:
        f.write(str(test))
    with pytest.raises(Exception):
        pytest.raises(
            models_resource.upload_model(name, accuracy=.123, loss=.123))
    if os.path.exists(name):
        os.remove(name)


# Negative test
def test_model_naming_rule(models_resource, test):
    name = "adsfsf,s=.h5"
    with open(name, 'w') as f:
        f.write(str(test))
    with pytest.raises(Exception):
        pytest.raises(
            models_resource.upload_model(name, accuracy=.123, loss=.123))
    if os.path.exists(name):
        os.remove(name)




# # Negative test
# def test_model_limit(models_resource):
#     name = 'limit_model'
#     if not os.path.exists(name):
#         f = open(name, "wb")
#         # create a file 2G +1 bytes
#         f.seek((2 * 1024 * 1024 * 1024 + 1) - 1)
#         f.write(b"\0")
#         f.close()
#     with pytest.raises(Exception):
#         pytest.raises(
#             models_resource.upload_model(name, accuracy=.123, loss=.123))

