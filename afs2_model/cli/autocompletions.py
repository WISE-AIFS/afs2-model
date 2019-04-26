from pathlib import Path

from .serializers import AFSClientSerializer
from .utils import afs_client_setup, instance_setup, model_repo_setup


def autocompletion_list_instances(ctx, args, incomplete):
    afs_client = afs_client_setup()
    instance_list = [
        instance.uuid
        for instance in afs_client.instances()
        if incomplete in instance.uuid
    ]
    AFSClientSerializer().serialization(afs_client)

    return instance_list


def autocompletion_list_model_repo(ctx, args, incomplete):
    instance = instance_setup()
    model_repos = [
        model_repo.name
        for model_repo in instance.model_repositories()
        if incomplete in model_repo.name
    ]
    AFSClientSerializer().serialization(
        afs_client=instance._resource_client._afs_client
    )

    return model_repos


def autocompletion_list_models(ctx, args, incomplete):
    model_repo_name = args[-1]
    model_repo = model_repo_setup(model_repo_name)
    models = [model.name for model in model_repo.models() if incomplete in model.name]
    AFSClientSerializer().serialization(
        afs_client=model_repo._resource_client._afs_client
    )

    return models


def autocompletion_lsit_files(ctx, args, incomplete):
    path = Path(incomplete)
    if path.is_file():
        return [str(path)]

    elif path.is_dir():
        return [str(file_path) for file_path in path.iterdir()]

    else:
        return [
            str(file_path)
            for file_path in path.parent.iterdir()
            if str(file_path).startswith(incomplete)
        ]
