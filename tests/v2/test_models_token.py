from uuid import UUID
import pytest


def test_token_create_model_repo(afs_models_token, delete_model_respository):
    create_resp = afs_models_token.create_model_repo(
        model_repository_name="test_model_repository"
    )
    assert isinstance(UUID(create_resp), UUID)


def test_token_get_model_repo_id(
    afs_models_token, model_repository, delete_model_respository
):
    get_resp = afs_models_token.get_model_repo_id(
        model_repository_name="test_model_repository"
    )
    assert get_resp == model_repository


def test_token_delete_model_repo(afs_models_token, model_repository):
    delete_resp = afs_models_token.delete_model_repository(
        model_repository_name="test_model_repository"
    )
    assert delete_resp == True
    resp = afs_models_token.get_model_repo_id(
        model_repository_name="test_model_repository"
    )
    assert resp == None


def test_token_create_model(afs_models_token, delete_mr_and_model, model_file):
    resp = afs_models_token.upload_model(
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


def test_token_get_model_id(afs_models_token, model, delete_mr_and_model, model_file):
    get_resp = afs_models_token.get_model_id(
        model_name="test_model",
        model_repository_name="test_model_repository",
        last_one=True,
    )
    assert get_resp == model["uuid"]


def test_token_delete_model(afs_models_token, model, delete_model_respository):
    resp = afs_models_token.delete_model(
        model_name="test_model", model_repository_name="test_model_repository"
    )
    assert resp == True
    get_resp = afs_models_token.get_model_id(
        model_name="test_model",
        model_repository_name="test_model_repository",
        last_one=True,
    )
    assert get_resp == None


def test_token_get_model_info(afs_models_token, model, delete_mr_and_model):
    resp = afs_models_token.get_model_info(
        model_name="test_model", model_repository_name="test_model_repository"
    )
    assert resp["uuid"] == model["uuid"]


def test_token_get_latest_model_info(afs_models_token, model, delete_mr_and_model):
    resp = afs_models_token.get_latest_model_info(
        model_repository_name="test_model_repository"
    )
    assert resp["uuid"] == model["uuid"]


def test_token_download_model(afs_models_token, model, delete_mr_and_model):
    resp = afs_models_token.download_model(
        save_path="download_model",
        model_repository_name="test_model_repository",
        model_name="test_model",
    )
    assert resp == True
    with open("download_model", "r") as f:
        content = f.read()
    assert content == "unit test"
