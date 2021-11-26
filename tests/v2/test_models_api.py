from uuid import UUID
import pytest

def test_download_model(test_env, afs_models, model, delete_mr_and_model, model_repository_name):

    resp = afs_models.api_download_model(
        instance_id=instance_id, 
        model_repository_id=model_repository_id, 
        model_id=model_id, 
        save_path="download_model.h5"
    )

    assert resp == True
    with open("download_model.h5", "r") as f:
        content = f.read()
    assert content == "unit test"
