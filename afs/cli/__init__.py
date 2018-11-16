import json

import click

from ..client import EIPaaSAFSSession
from ..parsers import manifest_parser


@click.group()
@click.option('--verify', default=False)
@click.pass_context
def cli(ctx, verify):
    ctx.obj = EIPaaSAFSSession(verify)


@cli.command()
@click.argument('target_endpoint')
@click.argument('username')
@click.argument('password')
@click.pass_obj
def login(session, target_endpoint, username, password):
    session.login(target_endpoint=target_endpoint, username=username, password=password)


@cli.command()
@click.pass_obj
def service_instances(session):
    service_instances = session.list_service_instances()
    for service_instance in service_instances:
        click.echo(service_instance)


@cli.command()
@click.option('-s', '--service_instance_id', default=None)
@click.pass_obj
def target(session, service_instance_id):
    result = session.target(service_instance_id=service_instance_id)
    if result:
        click.echo(json.dumps(result, indent=4))


@cli.command()
@click.argument('source_path', default='./')
@click.option('-f', '--manifest', default='./manifest.yml')
@click.option('--name', default=None)
@click.pass_obj
def push(session, source_path, manifest, name):
    session.push(source_path=source_path, manifest_path=manifest, name=name)


@cli.command()
@click.argument('notebook_path')
@click.argument('pypi_endpoint')
@click.option('-o', '--output_dir', default='./')
@click.option('-m', '--manifest_yaml', default=False)
@click.option('-s', '--afs_sdk_version', default=None)
@click.pass_obj
def parse_notebook(session, notebook_path, pypi_endpoint, output_dir, manifest_yaml, afs_sdk_version):
    manifest_parser(notebook_path, pypi_endpoint, output_dir, manifest_yaml, afs_sdk_version)