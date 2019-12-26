import os, pytest, uuid, json
from tests.mock_requests import MockResponse
from dotenv import load_dotenv
from afs import models
import time

@pytest.fixture(scope="session")
def model_file():
    with open("unit_test_model", "w") as f:
        f.write("unit test")
    yield

    os.remove("unit_test_model")
    if os.path.exists("delete_mr_and_model"):
        os.remove("delete_mr_and_model")


@pytest.fixture(scope="session")
def model_repository_name():
    return "mr_{0}".format(time.strftime("%H-%M-%S"))


@pytest.fixture(scope="function")
def afs_models(test_env):
    my_models = models()
    yield my_models


@pytest.fixture(scope="function")
def afs_models_blob(test_env):
    my_models = models()
    blob_endpoint = os.getenv("blob_endpoint", None)
    encode_blob_accessKey = os.getenv("blob_accessKey", None)
    encode_blob_secretKey = os.getenv("blob_secretKey", None)

    my_models.set_blob_credential(
        blob_endpoint, encode_blob_accessKey, encode_blob_secretKey
    )
    yield my_models


@pytest.fixture(scope="function")
def model_repository(afs_models, model_repository_name):
    yield afs_models.create_model_repo(model_repository_name=model_repository_name)


@pytest.fixture(scope="function")
def clean_mr(afs_models, model_repository_name):
    try:
        afs_models.delete_model_repository(model_repository_name=model_repository_name)
    except Exception as e:
        print(e)

@pytest.fixture(scope="function")
def model(clean_mr, afs_models, model_repository, model_file, model_repository_name):
    yield afs_models.upload_model(
        model_path="unit_test_model",
        extra_evaluation={"extra_loss": 1.23},
        model_repository_name=model_repository_name,
        model_name="test_model",
    )


@pytest.fixture(scope="function")
def delete_model_respository(afs_models, model_repository_name):
    yield
    afs_models.delete_model_repository(model_repository_name=model_repository_name)


@pytest.fixture(scope="function")
def delete_mr_and_model(afs_models, model_repository_name):
    yield
    try:
        afs_models.delete_model(
            model_name="test_model", model_repository_name=model_repository_name
        )
    except Exception as e:
        pass

    try:
        afs_models.delete_model_repository(
            model_repository_name=model_repository_name
        )
    except Exception as e:
        pass


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
        # f.seek((301 * 1024 * 1024 + 1) - 1)
        f.seek((1 * 1024 * 1024 + 1) - 1)
        f.write(b"\0")
        f.close()

    yield big_model_filename


@pytest.fixture(scope="function")
def afs_models_with_error_blob():
    my_models = models()
    blob_endpoint = os.getenv("blob_endpoint", None)
    encode_blob_accessKey = os.getenv("blob_accessKey", None)
    encode_blob_secretKey = "NDhkZTU1MGFjOTEwNGI3MTk4N2RjZGQ5ZWFjMTI0OTk="

    encode_blob_accessKey = os.getenv("blob_accessKey", None)
    my_models.set_blob_credential(
        blob_endpoint, encode_blob_accessKey, encode_blob_secretKey
    )
    yield my_models


@pytest.fixture(scope="function")
def afs_models_token(test_param_token):
    my_models = models(
        target_endpoint=test_param_token["afs_url"],
        instance_id=test_param_token["instance_id"],
        token=test_param_token["token"],
    )
    yield my_models


@pytest.fixture(scope="session")
def model_metafile():
    with open("unit_test_metafile", "w") as f:
        f.write("unit test")
    yield "unit_test_metafile"

    if os.path.exists("unit_test_metafile"):
        os.remove("unit_test_metafile")


@pytest.fixture(scope="function")
def delete_mr_and_metafile(afs_models, model_repository_name):
    yield
    try:
        afs_models.delete_model_metafile(
            name="test_metafile", model_repository_name=model_repository_name
        )
    except Exception as e:
        print(e)

    try:
        afs_models.delete_model_repository(
            model_repository_name=model_repository_name
        )
    except Exception as e:
        pass
