import os
import pytest

def test_upload_model(models_resource,  models_path, test):
    # p=models_path
    # p.write(str(test))
    name = 'test_model.h5'
    with open(name, 'w') as f:
        f.write(str(test))
    models_resource.upload_model(name, accuracy=.123, loss=.123)
    if os.path.exists(name):
        os.remove(name)

def test_download_model(models_resource, conf_resource, models_path, test):
    name = 'test_model.h5'
    try:
        models_resource.download_model(name, model_name=conf_resource['model_name'])
        assert os.path.exists(name)

        with open(name, 'r') as f:
            content = f.read()
        assert str(test) == content
    except Exception as e:
        pass
    finally:
        if os.path.exists(name):
            os.remove(name)

def test_model_naming_length(models_resource, models_path_error, test):
    a = ['a' for i in range(100)]
    name = '.'.join(a)
    with open(name, 'w') as f:
        f.write(str(test))
    with pytest.raises(Exception):
        pytest.raises(models_resource.upload_model(name, accuracy=.123, loss=.123))
    if os.path.exists(name):
        os.remove(name)

def test_model_naming_rule(models_resource, models_path_error, test):
    name = "adsfsf,s=.h5"
    with open(name, 'w') as f:
        f.write(str(test))
    with pytest.raises(Exception):
        pytest.raises(models_resource.upload_model(name, accuracy=.123, loss=.123))
    if os.path.exists(name):
        os.remove(name)
