import os
import pytest

def test_upload_model(models_resource,  models_path, test):
    p=models_path
    p.write(str(test))
    models_resource.upload_model(p, accuracy=.123, loss=.123)

def test_download_model(models_resource, conf_resource, models_path, test):
    models_resource.download_model(str(models_path), model_name=conf_resource['model_name'])
    assert os.path.exists(str(models_path))
    # with open(p, 'r') as f:
    #     content = f.read()
    # assert str(test) == content
