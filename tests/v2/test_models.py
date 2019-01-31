

def test_get_model_repo_id(mocker, mocker_models, mock_api_v2_resource, model_repository_name, model_name, model_repository_list_response):
    mocker.patch.object(mocker_models, '_get', return_value=model_repository_list_response)
    model_reop_id = mocker_models.get_model_repo_id(model_repository_name=model_repository_name)
    assert model_reop_id == "1a3a9596-8ee8-44b6-94f8-56ba70169300"


def test_get_model_id(mocker, mocker_models, model_repository_name, model_name, model_list_response):
    # mocker.patch.object(mocker_models, 'get_model_repo_id', return_value='123')
    mocker.patch.object(mocker_models, '_get', return_value=model_list_response)
    model_id = mocker_models.get_model_id(model_repository_name=model_repository_name, last_one=True)
    assert model_id == "b8ed105e-c0b8-4b39-a453-0efd3259aafe"


def test_upload_model(mocker, mocker_models, mock_api_v2_resource, model_repository_name, model_name, model_response):
    mocker.patch.object(mocker_models, '_create', return_value=model_response)
    assert mocker_models.upload_model(
        model_path=model_name,
        accuracy=0.1,
        loss=0.2,
        tags={"machine": "01"},
        extra_evaluation={"metric": 1},
        model_repository_name=model_repository_name,
        model_name=model_name) == True


def test_create_model_repo(mocker, mock_api_v2_resource, model_repository_name, mocker_models, model_name, model_repository_response):
    mocker.patch.object(mocker_models, '_create', return_value=model_repository_response)
    assert mocker_models.create_model_repo(model_name) == "11cc3faf-cd24-4d93-8f9a-09dd731f5397"


def test_get_latest_model_info(mocker, mock_api_v2_resource, model_repository_name, mocker_models, model_name, model_list_response):
    mocker.patch.object(mocker_models, '_get', return_value=model_list_response)
    resp = mocker_models.get_latest_model_info(model_repository_name)

    assert isinstance(resp, dict)
    assert 'uuid' in resp
    assert 'name' in resp
    assert 'owner' in resp
    assert 'created_at' in resp
    assert 'parameters' in resp
    assert 'tags' in resp
    assert 'evaluation_result' in resp
