from uuid import UUID
import pytest


def test_create_model_repo(test_env, clean_mr, afs_models, delete_model_respository, model_repository_name):
    create_resp = afs_models.create_model_repo(
        model_repository_name=model_repository_name
    )
    assert isinstance(UUID(create_resp), UUID)


def test_get_model_repo_id(
    test_env, afs_models, model_repository, delete_model_respository, model_repository_name
):
    get_resp = afs_models.get_model_repo_id(
        model_repository_name=model_repository_name
    )
    assert get_resp == model_repository


def test_delete_model_repo(test_env, afs_models, model_repository, model_repository_name):
    delete_resp = afs_models.delete_model_repository(
        model_repository_name=model_repository_name
    )
    assert delete_resp == True
    resp = afs_models.get_model_repo_id(model_repository_name=model_repository_name)
    assert resp == None