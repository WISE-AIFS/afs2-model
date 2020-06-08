from uuid import UUID
import pytest


def test_create_model(test_env, afs_models, clean_mr, delete_mr_and_model, model_file, model_repository_name):
    resp = afs_models.upload_model(
        model_path="unit_test_model",
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        extra_evaluation={"extra_loss": 1.23},
        model_repository_name=model_repository_name,
        model_name="test_model",
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp
    assert "feature_importance" in resp
    assert "coefficient" in resp

def test_get_model_id(test_env, afs_models, model, delete_mr_and_model, model_file, model_repository_name):
    get_resp = afs_models.get_model_id(
        model_name="test_model",
        model_repository_name=model_repository_name,
        last_one=True,
    )
    assert get_resp == model["uuid"]


def test_delete_model(test_env, afs_models, model, delete_model_respository, model_repository_name):
    resp = afs_models.delete_model(
        model_name="test_model", model_repository_name=model_repository_name
    )
    assert resp == True
    get_resp = afs_models.get_model_id(
        model_name="test_model",
        model_repository_name=model_repository_name,
        last_one=True
    )
    assert get_resp == None


def test_get_model_info(test_env, afs_models, model, delete_mr_and_model, model_repository_name):
    resp = afs_models.get_model_info(
        model_name="test_model", model_repository_name=model_repository_name
    )
    assert resp["uuid"] == model["uuid"]


def test_get_latest_model_info(test_env, afs_models, model, delete_mr_and_model, model_repository_name):
    resp = afs_models.get_latest_model_info(
        model_repository_name=model_repository_name
    )
    assert resp["uuid"] == model["uuid"]


def test_download_model(test_env, afs_models, model, delete_mr_and_model, model_repository_name):
    resp = afs_models.download_model(
        save_path="download_model.h5",
        model_repository_name=model_repository_name,
        model_name="test_model",
    )
    assert resp == True
    with open("download_model.h5", "r") as f:
        content = f.read()
    assert content == "unit test"


def test_create_firehose_apm_model(
    test_env, afs_models, clean_mr, apm_node_env, delete_mr_and_model, model_file, model_repository_name
):
    resp = afs_models.upload_model(
        model_path="unit_test_model",
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        model_repository_name=model_repository_name,
        model_name="test_model",
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp
    assert "apm_node" in resp["tags"]
    assert "feature_importance" in resp
    assert "coefficient" in resp
    assert "3" in resp["tags"]["apm_node"]

    get_resp = afs_models.get_model_id(
        model_name="test_model",
        model_repository_name=model_repository_name,
        last_one=True,
    )
    assert get_resp == resp["uuid"]


def test_error1_create_firehose_apm_model(
    test_env, afs_models, clean_mr, error1_apm_node_env, delete_mr_and_model, model_file, model_repository_name
):
    resp = afs_models.upload_model(
        model_path="unit_test_model",
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        model_repository_name=model_repository_name,
        model_name="test_model",
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp
    assert "feature_importance" in resp
    assert "coefficient" in resp

    get_resp = afs_models.get_model_id(
        model_name="test_model",
        model_repository_name=model_repository_name,
        last_one=True,
    )
    assert get_resp == resp["uuid"]

def test_connect_blob_error_create_model(
    test_env, afs_models_with_error_blob, big_model, delete_mr_and_model, model_repository_name
):
    with pytest.raises(Exception):
        assert afs_models_with_error_blob.upload_model(
            model_path=big_model,
            accuracy=1.0,
            loss=1.0,
            tags={"tag_key": "tag_value"},
            model_repository_name=model_repository_name,
            model_name="test_model",
            blob_mode=True,
        )


def test_create_model_with_datasetid_target(test_env, afs_models, clean_mr, delete_mr_and_model, model_file, model_repository_name):
    resp = afs_models.upload_model(
        model_path="unit_test_model",
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        extra_evaluation={"extra_loss": 1.23},
        model_repository_name=model_repository_name,
        model_name="test_model",
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp
    assert "feature_importance" in resp
    assert "coefficient" in resp
    assert "dataset_id" in resp
    assert "afs_target" in resp
    print(resp)

def test_create_model_with_ft_and_cofficient(test_env, afs_models, clean_mr, delete_mr_and_model, model_file, model_repository_name):

    feature_importance = [
        {'feature': 'petal_length', 'feature_importance': 0.9473576807512394}, 
        {'feature': 'petal_width',  'feature_importance': 0.038191635936882906}, 
        {'feature': 'sepal_length', 'feature_importance': 0.011053241240641932}, 
        {'feature': 'sepal_width',  'feature_importance': 0.0033974420712357825}
    ]

    coefficient = [
        {'feature': 'B-0070-0068-1-FN66F_strength', 'coefficient': -4.730741400252476}, 
        {'feature': 'B-0070-0068-1-FN66F_vendor', 'coefficient': -0.9335123601234512}, 
        {'feature': 'B-0070-0068-1-FN66F_tensile','coefficient': 0.16411707246054036}, 
        {'feature': 'B-0070-0068-1-FN66F_lot','coefficient': -0.08745686004816221}, 
        {'feature': 'Machine','coefficient': 0.015048547152059243}, 
        {'feature': 'Lot','coefficient': -0.010971975766858174}, 
        {'feature': 'RPM','coefficient': 0.0003730247816832932}, 
        {'feature': 'record_purpose','coefficient': 0.0}
    ]

    resp = afs_models.upload_model(
        model_path="unit_test_model",
        accuracy=1.0,
        loss=1.0,
        tags={"tag_key": "tag_value"},
        extra_evaluation={"extra_loss": 1.23},
        feature_importance=feature_importance,
        coefficient=coefficient,
        model_repository_name=model_repository_name,
        model_name="test_model",
    )
    assert isinstance(resp, dict)
    assert "uuid" in resp
    assert "name" in resp
    assert "created_at" in resp
    assert "tags" in resp
    assert "evaluation_result" in resp
    assert "feature_importance" in resp
    assert "coefficient" in resp
    print(resp)
