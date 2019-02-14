import os, pytest, uuid
from tests.mock_requests import MockResponse

@pytest.fixture()
def mocker_models(v2_env, mock_api_v2_resource):
    from afs import models
    yield models()


@pytest.fixture(scope='session')
def test():
    return uuid.uuid4()


@pytest.fixture(scope='module')
def model_name(test):
    test_model = 'test_model.h5'
    if os.path.exists(test_model):
        os.remove(test_model)
    with open(test_model, 'w') as f:
        f.write(str(test))

    yield test_model

    os.remove(test_model)


@pytest.fixture()
def model_repository_name(mocker, mocker_models):
    mocker.patch.object(mocker_models, 'get_model_repo_id', return_value='1a3a9596-8ee8-44b6-94f8-56ba70169300')
    mocker.patch.object(mocker_models, 'repo_id', return_value='1a3a9596-8ee8-44b6-94f8-56ba70169300')
    return 'test_model_repo'


@pytest.fixture()
def model_response():
    return MockResponse(text="""
    {
      "uuid": "ce7e5378-eeb1-421a-b2cd-5b62288d8cb9",
      "name": "test_model.h5",
      "owner": "660939a7-edfb-4873-ba8a-1674ddb602d5",
      "model_repository": "1a3a9596-8ee8-44b6-94f8-56ba70169300",
      "evaluation_result": {
        "metrics": 1,
        "loss": 0.1,
        "accuracy": "0.2"
      },
      "parameters": {
      },
      "tags": {
        "machine": "01"      
      },
      "created_at": "2019-01-31T08:14:57.750000+00:00"
    }""", status_code=200)


@pytest.fixture()
def model_list_response():
    return MockResponse(text="""
    {
          "pagination": {
            "start": 0,
            "limit": 10,
            "total": 1
          },
          "resources": [
            {
              "uuid": "b8ed105e-c0b8-4b39-a453-0efd3259aafe",
              "name": "test_model.h5",
              "owner": "660939a7-edfb-4873-ba8a-1674ddb602d5",
              "model_repository": "1a3a9596-8ee8-44b6-94f8-56ba70169300",
              "evaluation_result": {
                "accuracy": 0.1,
                "loss": 0.2,
                "metrics": 1
              },
              "parameters": {
                "a": 1,
                "b": 2
              },
              "tags": {
                "machine": "01"
              },
              "created_at": "2019-01-15T10:07:54.966000+00:00"
            }
          ]
    }""", status_code=200)


@pytest.fixture()
def model_repository_list_response():
    return MockResponse(text="""
            {
              "pagination": {
                "start": 0,
                "limit": 10,
                "total": 1
              },
              "resources": [
                {
                  "uuid": "1a3a9596-8ee8-44b6-94f8-56ba70169300",
                  "name": "test_model.h5",
                  "owner": "660939a7-edfb-4873-ba8a-1674ddb602d5",
                  "created_at": "2019-01-15T07:59:35.088000+00:00",
                  "total_models": 0,
                  "last_update": "2019-01-30T09:10:56.595000+00:00"
                }
              ]
            }
            """, status_code=200)


@pytest.fixture()
def model_repository_response():
    return MockResponse(text="""
    {
      "uuid": "11cc3faf-cd24-4d93-8f9a-09dd731f5397",
      "name": "test_model.h5",
      "owner": "75dca8a9-c6f7-4440-b8df-16989c0abca9",
      "created_at": "2019-01-31T09:40:12.702000+00:00",
      "total_models": 0,
      "last_update": "2019-01-31T09:40:12.702000+00:00"
    }""", status_code=200)

