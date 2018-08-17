import pytest
import uuid
import os
from afs import models
from afs import services
from afs import config_handler

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), ".env_779f")
load_dotenv(dotenv_path=env_path)

@pytest.fixture()
def test():
    return uuid.uuid4()

@pytest.fixture(scope='class')
def models_resource():
    afs_models=models()
    yield afs_models

@pytest.fixture(scope='class')
def services_resource():
    afs_services=services()
    yield afs_services

@pytest.fixture(scope='class')
def config_handler_resource():
    afs_config_handler = config_handler_resource()
    yield afs_config_handler

@pytest.fixture(scope='class')
def conf_resource():
    conf={ "model_name":"test_model.h5"}
    return conf

@pytest.fixture(scope="function")
def models_path(tmpdir):
    yield tmpdir.mkdir('data').join("test_model.h5")


