import pytest
import uuid
import os
from afs import models
import platform

sysstr = platform.system()
if (sysstr == "Windows"):
    from dotenv import Dotenv
    dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))  # Of course, replace by your correct path
    os.environ.update(dotenv)
elif (sysstr == "Linux"):
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)

@pytest.fixture()
def test():
    return uuid.uuid4()

@pytest.fixture(scope='class')
def models_resource():
    afs_models=models()

    yield afs_models

@pytest.fixture(scope='class')
def conf_resource():
    conf={ "model_name":"test_model.h5"}
    return conf

@pytest.fixture(scope="class")
def models_file(tmpdir):
    f1 = tmpdir.mkdir