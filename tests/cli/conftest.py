import os
import shlex
import shutil

from datetime import datetime
from pathlib import Path

import pytest

from afs2_model.cli.serializers import CONFIG_PATH, ROOT_PATH
from click.testing import CliRunner


@pytest.fixture(scope="session", autouse=True)
def remove_config():
    yield
    shutil.rmtree(str(ROOT_PATH))


@pytest.fixture()
def cli():

    from afs2_model.cli import cli

    yield cli

    try:
        CONFIG_PATH.unlink()
    except:
        pass


@pytest.fixture()
def cli_runner():
    yield CliRunner()


@pytest.fixture(scope="session")
def loged_cli():
    from afs2_model.cli import cli

    api_endpoint = os.getenv("TEST_AFS_API_SERVER", "")
    username = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PASSWORD")

    cmd = "login -a {} -u {} -p {}".format(api_endpoint, username, password)

    runner = CliRunner()
    runner.invoke(cli, shlex.split(cmd))
    yield cli


@pytest.fixture()
def target_instance(loged_cli, cli_runner, instance_id):
    cmd = "target {}".format(instance_id)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))
    yield


@pytest.fixture()
def model_repo_name(target_instance):
    yield "sdk_cli_model_repo_test_fixture_{}".format(datetime.utcnow().timestamp())


@pytest.fixture()
def model_repository(
    loged_cli, cli_runner, target_instance, model_repo_name, remove_model_repository
):
    cmd = "create-model-repo {}".format(model_repo_name)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    yield model_repo_name


@pytest.fixture()
def remove_model_repository(loged_cli, cli_runner, target_instance, model_repo_name):
    yield

    cmd = "delete-model-repo {}".format(model_repo_name)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))


@pytest.fixture()
def model_name():
    yield "sdk_models_test_fixture_{}".format(datetime.utcnow().timestamp())


@pytest.fixture()
def model_path():
    model_path = os.path.join(os.path.dirname(__file__), "model_fixture")
    with open(model_path, "w") as f:
        f.write("model_fixture")

    yield model_path

    os.remove(model_path)


@pytest.fixture()
def model(
    loged_cli,
    cli_runner,
    target_instance,
    model_repository,
    model_name,
    model_path,
    remove_model,
):
    cmd = "create-model {} {} {}".format(model_repository, model_name, model_path)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    yield model_name


@pytest.fixture()
def remove_model(loged_cli, cli_runner, target_instance, model_repository, model_name):
    yield

    cmd = "delete-modle {} {}".format(model_repository, model_name)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))
