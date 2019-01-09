from tests.mock_requests import MockResponse


# v2 API unit_test
def test_upload_model_v2(mocker, test, mock_api_v2_resource, mock_models, model_name):
    mocker.patch.object(mock_models, 'switch_repo', return_value=None)
    mocker.patch.object(mock_models, 'create_model_repo', return_value='123')
    mocker.patch.object(mock_models, '_put', return_value=MockResponse(status_code=200, text="""
    {
      "uuid": "c2714f44-fab9-4bde-afc9-7b3ab40cd431",
      "name": "test_model.h5",
      "created_at": "2018-08-20 09:16:18",
      "models": [
        "b5e8399d-3a95-42a5-88f5-79b8cdeb4045"
      ]
    }"""))
    assert mock_models.upload_model(model_name, accuracy=.123, loss=.123) == True

# v2 API unit_test
def test_create_model_repo_v2(mocker, mock_api_v2_resource, mock_models, model_name):
    mocker.patch.object(mock_models, '_create', return_value=MockResponse(text="""
    {
        "uuid": "c2714f44-fab9-4bde-afc9-7b3ab40cd431",
        "name": "test_model.h5",
        "created_at": "2018-08-20 09:16:18",
        "models": []
    }""", status_code=200))
    assert mock_models.create_model_repo(model_name) == "c2714f44-fab9-4bde-afc9-7b3ab40cd431"

# v2 API unit_test
def test_switch_repo_v2(mocker, mock_api_v2_resource, mock_models, model_name):
    mocker.patch.object(mock_models, '_get', return_value=MockResponse(text="""
    [{
      "uuid": "c2714f44-fab9-4bde-afc9-7b3ab40cd431",
      "name": "test_model.h5",
      "created_at": "2018-08-20 09:16:18",
      "models": [
        "b5e8399d-3a95-42a5-88f5-79b8cdeb4045"
      ]
    }]
      """, status_code=200)
    )
    assert mock_models.switch_repo(model_name) == "c2714f44-fab9-4bde-afc9-7b3ab40cd431"


def test_get_latest_model_info_v2(mocker, mock_api_v2_resource, mock_models, model_name):
    mocker.patch.object(mock_models, '_get', return_value=MockResponse(text="""
        {
            "evaluation_result": {
                "accuracy": 0.4,
                "loss": 0.3
            },
            "tags": {
                "adder": "71"
            },
            "created_at": "2018-11-29 09:40:08"
        }
        """, status_code=200)
    )
    mocker.patch.object(mock_models, 'switch_repo', return_value='c2714f44-fab9-4bde-afc9-7b3ab40cd431')
    model_info = mock_models.get_latest_model_info(model_name)
    assert 'evaluation_result' in model_info
    assert 'tags' in model_info
    assert 'created_at' in model_info
