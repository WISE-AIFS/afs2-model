import os
import shlex

import pytest

from click._bashcomplete import get_choices

from afs2_model import __version__


def test_cli_version(cli, cli_runner):
    cmd = "--version"
    result = cli_runner.invoke(cli, shlex.split(cmd))
    assert result.exit_code == 0
    assert result.output == __version__ + "\n"


def test_cli_login(cli, cli_runner):
    api_endpoint = os.getenv("TEST_AFS_API_SERVER", "")
    username = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PASSWORD")

    cmd = "login -a {} -u {} -p {}".format(api_endpoint, username, password)

    result = cli_runner.invoke(cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert (
        result.output
        == "Login to {api_endpoint} as user {username} succeeded\n".format(
            api_endpoint=api_endpoint, username=username
        )
    )


def test_cli_login_interactive(cli, cli_runner):
    api_endpoint = os.getenv("TEST_AFS_API_SERVER", "")
    username = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PASSWORD")

    cmd = "login"
    stdin = "{}\n{}\n{}\n".format(api_endpoint, username, password)

    result = cli_runner.invoke(cli, shlex.split(cmd), input=stdin)

    assert result.exit_code == 0
    assert (
        result.output
        == "Api endpoint: {api_endpoint}\nUsername: {username}\nPassword: \n"
        "Login to {api_endpoint} as user {username} succeeded\n".format(
            api_endpoint=api_endpoint, username=username
        )
    )


def test_cli_list_instances(loged_cli, cli_runner):
    cmd = "instances"
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert result.output.count("\n") >= 1


def test_cli_target(loged_cli, cli_runner, instance_id):
    cmd = "target {}".format(instance_id)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert result.output == "Target to instance {} succeeded\n".format(instance_id)


def test_cli_target_autocompletion(loged_cli, cli_runner, instance_id):
    cmd = "target"
    args = shlex.split(cmd)
    incomplete = instance_id[0:3]
    completions = get_choices(loged_cli, "dummy", args, incomplete)

    assert (instance_id, None) in completions


def test_cli_list_model_repos(loged_cli, target_instance, cli_runner, model_repository):
    cmd = "model-repos"
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert result.output.count("\n") >= 1


def test_cli_create_model_repo(
    loged_cli, cli_runner, model_repo_name, remove_model_repository
):
    cmd = "create-model-repo {}".format(model_repo_name)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert result.output == "Create model repository {} succeeded\n".format(
        model_repo_name
    )


def test_cli_delete_model_repo(loged_cli, cli_runner, model_repository):
    cmd = "delete-model-repo {}".format(model_repository)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert result.output == "Delete model repository {} succeeded\n".format(
        model_repository
    )


def test_cli_delete_model_repos_autocompletion(loged_cli, cli_runner, model_repository):
    cmd = "delete-model-repo"
    args = shlex.split(cmd)
    incomplete = model_repository[0:3]
    completions = get_choices(loged_cli, "dummy", args, incomplete)

    assert (model_repository, None) in completions


def test_cli_list_models(loged_cli, cli_runner, model_repository, model):
    cmd = "models {}".format(model_repository)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert result.output.count("\n") >= 1


def test_cli_create_model(
    loged_cli, cli_runner, model_repository, model_name, model_path, remove_model
):
    cmd = "create-model {} {} {}".format(model_repository, model_name, model_path)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert result.output == "Create model {} succeeded\n".format(model_name)


@pytest.mark.parametrize(
    "model_path,incomplete",
    [
        (("README.md", None), "RE"),
        (("README.md", None), "README.md"),
        (("afs2_model/__init__.py", None), "afs/"),
    ],
)
def test_cli_create_model_autocompletion(
    loged_cli, cli_runner, model_repository, model_name, model_path, incomplete
):
    cmd = "create-model {} {}".format(model_repository, model_name)
    args = shlex.split(cmd)
    completions = get_choices(loged_cli, "dummy", args, incomplete)

    assert model_path in completions


def test_cli_delete_model(loged_cli, cli_runner, model_repository, model):
    cmd = "delete-model {} {}".format(model_repository, model)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert result.output == "Delete model {} succeeded\n".format(model)


def test_cli_delete_model_autocompletion(
    loged_cli, cli_runner, model_repository, model
):
    cmd = "delete-model"
    args = shlex.split(cmd)
    incomplete = model_repository[0:3]
    completions = get_choices(loged_cli, "dummy", args, incomplete)

    assert (model_repository, None) in completions

    cmd = "delete-model {}".format(model_repository)
    args = shlex.split(cmd)
    incomplete = model[0:3]
    completions = get_choices(loged_cli, "dummy", args, incomplete)

    assert (model, None) in completions


def test_cli_download_model(loged_cli, cli_runner, model_repository, model):
    cmd = "download-model {} {}".format(model_repository, model)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert result.output == "Download model {} to path {} succeeded\n".format(
        model, model
    )
    assert os.path.isfile(model)

    os.remove(model)


def test_cli_download_model_with_path(loged_cli, cli_runner, model_repository, model):
    download_path = "sdk_cli_test_download_model.pkl"
    cmd = "download-model {} {} -p {}".format(model_repository, model, download_path)
    result = cli_runner.invoke(loged_cli, shlex.split(cmd))

    assert result.exit_code == 0
    assert result.output == "Download model {} to path {} succeeded\n".format(
        model, download_path
    )
    assert os.path.isfile(download_path)

    os.remove(download_path)
