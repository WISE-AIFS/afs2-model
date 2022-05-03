def test_download_model_from_blob(test_env, afs_models, model, blob_info, delete_model_respository):
    resp = afs_models.download_model_from_blob(
        instance_id=model['owner'], 
        model_repository_id=model['model_repository'], 
        model_id=model['uuid'], 
        save_path="download_model.h5",
        blob_endpoint=blob_info['blob_endpoint'],
        blob_accessKey=blob_info['blob_accessKey'],
        blob_secretKey=blob_info['blob_secretKey'],
        bucket_name=blob_info['bucket_name'],
    )

    assert resp == True
    with open("download_model.h5", "r") as f:
        content = f.read()
    assert content == "unit test"
