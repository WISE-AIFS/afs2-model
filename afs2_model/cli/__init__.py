import os

import click

from click.exceptions import BadParameter, UsageError

from afs2_model import AFSClient, __version__

from .autocompletions import (
    autocompletion_list_instances,
    autocompletion_list_model_repo,
    autocompletion_list_models,
    autocompletion_lsit_files,
)
from .serializers import AFSClientSerializer
from .utils import afs_client_setup, instance_setup, model_repo_setup


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option(
    "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True
)
@click.option(
    "--ssl-verify/--skip-ssl-verify",
    default=True,
    help="To verify SSL of API endpoint or not. Default is True.",
)
@click.pass_context
def cli(ctx, ssl_verify):
    state = AFSClientSerializer().deserialization()
    state.update({"ssl": ssl_verify})
    ctx.obj = state


@cli.command()
@click.option("-a", "--api_endpoint", prompt=True)
@click.option("-u", "--username", prompt=True)
@click.option("-p", "--password", prompt=True, hide_input=True)
@click.pass_obj
def login(obj, api_endpoint, username, password):
    afs_client = AFSClient(
        api_endpoint=api_endpoint, username=username, password=password, ssl=obj["ssl"]
    )
    click.echo("Login to {} as user {} succeeded".format(api_endpoint, username))
    AFSClientSerializer().serialization(afs_client)


@cli.command()
@click.pass_obj
def instances(obj):
    afs_client = afs_client_setup(obj)
    for instance in afs_client.instances(limit=1000):
        click.echo(instance.uuid)


@cli.command()
@click.argument("instance_id", autocompletion=autocompletion_list_instances)
@click.pass_obj
def target(obj, instance_id):
    afs_client = afs_client_setup(state=obj)
    instance = afs_client.instances(instance_id)
    AFSClientSerializer().serialization(afs_client, instance)

    click.echo("Target to instance {} succeeded".format(instance_id))


@cli.command()
@click.pass_obj
def model_repos(obj):
    instance = instance_setup(state=obj)
    if not instance:
        raise UsageError("Please target a instance first.")

    model_repos = instance.model_repositories(limit=1000)
    AFSClientSerializer().serialization(
        afs_client=instance._resource_client._afs_client
    )

    for model_repo in model_repos:
        click.echo(model_repo.name)


@cli.command()
@click.argument("model_repo_name")
@click.pass_obj
def create_model_repo(obj, model_repo_name):
    instance = instance_setup(state=obj)
    if not instance:
        raise UsageError("Please target a instance first.")

    instance.model_repositories.create(name=model_repo_name)
    AFSClientSerializer().serialization(
        afs_client=instance._resource_client._afs_client
    )

    click.echo("Create model repository {} succeeded".format(model_repo_name))


@cli.command()
@click.argument("model_repo_name", autocompletion=autocompletion_list_model_repo)
@click.pass_obj
def delete_model_repo(obj, model_repo_name):
    model_repo = model_repo_setup(model_repo_name, state=obj)
    model_repo.delete()
    AFSClientSerializer().serialization(
        afs_client=model_repo._resource_client._afs_client
    )

    click.echo("Delete model repository {} succeeded".format(model_repo_name))


@cli.command()
@click.argument("model_repo_name", autocompletion=autocompletion_list_model_repo)
@click.pass_obj
def models(obj, model_repo_name):
    model_repo = model_repo_setup(model_repo_name, state=obj)
    models = model_repo.models(limit=1000)
    AFSClientSerializer().serialization(
        afs_client=model_repo._resource_client._afs_client
    )

    for model in models:
        click.echo(model.name)


@cli.command()
@click.argument("model_repo_name", autocompletion=autocompletion_list_model_repo)
@click.argument("model_name")
@click.argument("model_path", autocompletion=autocompletion_lsit_files)
@click.option(
    "-e",
    "--evalution_result",
    help="A JSON string to repersent evalution result of this model.",
)
@click.option("-t", "--tags", help="A JSON string to repersent tags of this model.")
@click.option(
    "-p",
    "--parameters",
    help="A JSON string to repersent training parameters of this model.",
)
@click.pass_obj
def create_model(
    obj,
    model_repo_name,
    model_name,
    model_path,
    evalution_result=None,
    tags=None,
    parameters=None,
):
    model_repo = model_repo_setup(model_repo_name, state=obj)

    try:
        model_repo.models.create(
            name=model_name,
            model_path=model_path,
            evalution_result=evalution_result,
            tags=tags,
            parameters=parameters,
        )

    except Exception as e:
        raise UsageError(e)

    AFSClientSerializer().serialization(
        afs_client=model_repo._resource_client._afs_client
    )

    click.echo("Create model {} succeeded".format(model_name))


def model_setup(model_repo_name, model_name, state=None):
    model_repo = model_repo_setup(model_repo_name, state=state)
    model = next(
        (model for model in model_repo.models() if model.name == model_name), None
    )

    if not model:
        raise BadParameter(
            "Model with name {} not found in model repository {}".format(
                model_name, model_repo_name
            )
        )

    AFSClientSerializer().serialization(
        afs_client=model_repo._resource_client._afs_client
    )
    return model


@cli.command()
@click.argument("model_repo_name", autocompletion=autocompletion_list_model_repo)
@click.argument("model_name", autocompletion=autocompletion_list_models)
@click.pass_obj
def delete_model(obj, model_repo_name, model_name):
    model = model_setup(model_repo_name, model_name, state=obj)

    try:
        model.delete()

    except Exception as e:
        raise UsageError(e)

    AFSClientSerializer().serialization(afs_client=model._resource_client._afs_client)

    click.echo("Delete model {} succeeded".format(model_name))


@cli.command()
@click.argument("model_repo_name", autocompletion=autocompletion_list_model_repo)
@click.argument("model_name", autocompletion=autocompletion_list_models)
@click.option("-p", "--model_path", help="The target file path to save model.")
@click.pass_obj
def download_model(obj, model_repo_name, model_name, model_path=None):
    if not model_path:
        model_path = model_name

    model = model_setup(model_repo_name, model_name, state=obj)
    try:
        model.download(model_path)
    except Exception as e:
        raise UsageError(e)

    AFSClientSerializer().serialization(afs_client=model._resource_client._afs_client)
    click.echo("Download model {} to path {} succeeded".format(model_name, model_path))
