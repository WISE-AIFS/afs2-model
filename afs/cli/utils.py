from click.exceptions import BadParameter, UsageError

from afs import AFSClient

from .serializers import AFSClientSerializer


def afs_client_setup(state=None):

    if not state:
        state = AFSClientSerializer().deserialization()

    attrs = ["api_endpoint", "api_version", "token"]
    if not all((True for attr in attrs)):
        raise UsageError("Please login first")

    afs_client = AFSClient(
        api_endpoint=state["api_endpoint"],
        api_version=state["api_version"],
        ssl=state["ssl"],
        token=state["token"],
    )

    return afs_client


def instance_setup(state=None, afs_client=None):
    if not state:
        state = AFSClientSerializer().deserialization()

    if not afs_client:
        afs_client = afs_client_setup(state)

    instance = state.get("instance_id", None)
    if instance:
        instance = afs_client.instances(instance)

    return instance


def model_repo_setup(model_repo_name, state=None, afs_client=None):
    instance = instance_setup(state=state)
    if not instance:
        raise UsageError("Please target a instance first.")

    model_repo = next(
        (
            model_repo
            for model_repo in instance.model_repositories()
            if model_repo.name == model_repo_name
        ),
        None,
    )

    if not model_repo:
        raise BadParameter(
            "Model repository with name {} not found".format(model_repo_name)
        )

    return model_repo
