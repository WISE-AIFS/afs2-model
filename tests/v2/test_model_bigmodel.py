
def test_create_big_model(test_env, afs_models_blob, big_model, delete_mr_and_model):
    resp = afs_models_blob.upload_model(
        model_path=big_model,
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        model_repository_name="test_model_repository",
        model_name="test_model",
        blob_mode=True,
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "parameters" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp
    assert "size" in resp
    assert resp["size"] > 1 * 1024 * 1024

    get_resp = afs_models_blob.get_model_id(
        model_name="test_model",
        model_repository_name="test_model_repository",
        last_one=True,
    )
    assert get_resp == resp["uuid"]


def test_create_big_model_env(test_env, afs_models, big_model, delete_mr_and_model):
    resp = afs_models.upload_model(
        model_path=big_model,
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        model_repository_name="test_model_repository",
        model_name="test_model",
        blob_mode=True,
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "parameters" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp
    assert "size" in resp
    assert resp["size"] > 1 * 1024 * 1024

    get_resp = afs_models.get_model_id(
        model_name="test_model",
        model_repository_name="test_model_repository",
        last_one=True,
    )
    assert get_resp == resp["uuid"]