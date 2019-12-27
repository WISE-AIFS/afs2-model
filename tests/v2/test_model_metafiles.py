def test_create_model_metafile(
    test_env, afs_models_blob, model_repository, model_metafile, delete_mr_and_metafile, model_repository_name
):
    resp = afs_models_blob.upload_model_metafile(
        file_path=model_metafile,
        name="test_metafile",
        model_repository_name=model_repository_name,
    )

    assert resp["status"] == "done"
