from uuid import UUID


def test_create_model_repo(afs_models, delete_model_respository):
    create_resp = afs_models.create_model_repo(
        model_repository_name="test_model_repository"
    )
    assert isinstance(UUID(create_resp), UUID)


def test_get_model_repo_id(afs_models, model_repository, delete_model_respository):
    get_resp = afs_models.get_model_repo_id(
        model_repository_name="test_model_repository"
    )
    assert get_resp == model_repository


def test_delete_model_repo(afs_models, model_repository):
    delete_resp = afs_models.delete_model_repository(
        model_repository_name="test_model_repository"
    )
    assert delete_resp == True
    resp = afs_models.get_model_repo_id(model_repository_name="test_model_repository")
    assert resp == None


def test_create_model(afs_models, delete_mr_and_model, model_file):
    resp = afs_models.upload_model(
        model_path="unit_test_model",
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        extra_evaluation={"extra_loss": 1.23},
        model_repository_name="test_model_repository",
        model_name="test_model",
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "parameters" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp


def test_get_model_id(afs_models, model, delete_mr_and_model, model_file):
    get_resp = afs_models.get_model_id(
        model_name="test_model",
        model_repository_name="test_model_repository",
        last_one=True,
    )
    assert get_resp == model["uuid"]


def test_delete_model(afs_models, model, delete_model_respository):
    resp = afs_models.delete_model(
        model_name="test_model", model_repository_name="test_model_repository"
    )
    assert resp == True
    get_resp = afs_models.get_model_id(
        model_name="test_model",
        model_repository_name="test_model_repository",
        last_one=True,
    )
    assert get_resp == None


def test_get_model_info(afs_models, model, delete_mr_and_model):
    resp = afs_models.get_model_info(
        model_name="test_model", model_repository_name="test_model_repository"
    )
    assert resp["uuid"] == model["uuid"]


def test_get_latest_model_info(afs_models, model, delete_mr_and_model):
    resp = afs_models.get_latest_model_info(
        model_repository_name="test_model_repository"
    )
    assert resp["uuid"] == model["uuid"]


def test_download_model(afs_models, model, delete_mr_and_model):
    resp = afs_models.download_model(
        save_path="download_model",
        model_repository_name="test_model_repository",
        model_name="test_model",
    )
    assert resp == True
    with open("download_model", "r") as f:
        content = f.read()
    assert content == "unit test"


def test_create_firehose_apm_model(
    afs_models, apm_node_env, delete_mr_and_model, model_file
):
    resp = afs_models.upload_model(
        model_path="unit_test_model",
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        model_repository_name="test_model_repository",
        model_name="test_model",
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "parameters" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp
    assert "apm_node" in resp["tags"]
    assert "3" in resp["tags"]["apm_node"]

    get_resp = afs_models.get_model_id(
        model_name="test_model",
        model_repository_name="test_model_repository",
        last_one=True,
    )
    assert get_resp == resp["uuid"]


def test_error1_create_firehose_apm_model(
        afs_models, error1_apm_node_env, delete_mr_and_model, model_file
):
    resp = afs_models.upload_model(
        model_path="unit_test_model",
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        model_repository_name="test_model_repository",
        model_name="test_model",
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "parameters" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp

    get_resp = afs_models.get_model_id(
        model_name="test_model",
        model_repository_name="test_model_repository",
        last_one=True,
    )
    assert get_resp == resp["uuid"]


def test_create_big_model(afs_models_blob, big_model, delete_mr_and_model):
    resp = afs_models_blob.upload_model(
        model_path=big_model,
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        model_repository_name="test_model_repository",
        model_name="test_model",
        blob_mode=True
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "parameters" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp
    assert "size" in resp
    print(resp['size'])
    assert resp["size"] > 1 * 1024 * 1024

    get_resp = afs_models_blob.get_model_id(
        model_name="test_model",
        model_repository_name="test_model_repository",
        last_one=True,
    )
    assert get_resp == resp["uuid"]
