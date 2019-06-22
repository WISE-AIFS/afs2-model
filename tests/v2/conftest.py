import os, pytest, uuid, json
from tests.mock_requests import MockResponse
from dotenv import load_dotenv
from afs import models

load_dotenv()


@pytest.fixture(scope="session")
def model_file():
    with open("unit_test_model", "w") as f:
        f.write("unit test")
    yield

    os.remove("unit_test_model")
    if os.path.exists("delete_mr_and_model"):
        os.remove("delete_mr_and_model")


@pytest.fixture(scope="function")
def afs_models():
    my_models = models()
    yield my_models


@pytest.fixture(scope="function")
def afs_models_blob():
    my_models = models()
    blob_endpoint = os.getenv("blob_endpoint", None)
    blob_accessKey = os.getenv("blob_accessKey", None)
    blob_secretKey = os.getenv("blob_secretKey", None)

    my_models.set_blob_credential(blob_endpoint, blob_accessKey, blob_secretKey)
    yield my_models


@pytest.fixture(scope="function")
def model_repository(afs_models):
    yield afs_models.create_model_repo(model_repository_name="test_model_repository")


@pytest.fixture(scope="function")
def model(afs_models, model_repository, model_file):
    yield afs_models.upload_model(
        model_path="unit_test_model",
        extra_evaluation={"extra_loss": 1.23},
        model_repository_name="test_model_repository",
        model_name="test_model",
    )


@pytest.fixture(scope="function")
def delete_model_respository(afs_models):
    yield
    afs_models.delete_model_repository(model_repository_name="test_model_repository")


@pytest.fixture(scope="function")
def delete_mr_and_model(afs_models):
    yield
    afs_models.delete_model(
        model_name="test_model", model_repository_name="test_model_repository"
    )
    afs_models.delete_model_repository(model_repository_name="test_model_repository")


@pytest.fixture(scope="function")
def apm_node_env():
    pai_data_dir = {"type": "apm-firehose", "data": {"machineIdList": [3]}}
    os.environ["PAI_DATA_DIR"] = json.dumps(pai_data_dir)
    yield
    del os.environ["PAI_DATA_DIR"]


@pytest.fixture(scope="function")
def error1_apm_node_env():
    pai_data_dir = "123"
    os.environ["PAI_DATA_DIR"] = pai_data_dir
    yield
    del os.environ["PAI_DATA_DIR"]


@pytest.fixture(scope="function")
def big_model():
    big_model_filename = "big_model.h5"
    if not os.path.exists(big_model_filename):
        f = open(big_model_filename, "wb")
        f.seek((301 * 1024 * 1024 + 1) - 1)
        f.write(b"\0")

    yield big_model_filename
