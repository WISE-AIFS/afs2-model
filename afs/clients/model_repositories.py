from .base import BaseResourceModel, BaseResourcesClient
from .exceptions import ModelRepositoriesClientError
from .models import ModelsClient


class ModelRepository(BaseResourceModel):
    """
    Resource model for Model Repositories resource of AFS v2 API.
    """

    def __init__(self, resource_client, *args, **kwargs):
        resource = "model_erpository"
        super().__init__(
            resource_client=resource_client, resource=resource, *args, **kwargs
        )

        self.models = ModelsClient(
            resource_client._afs_client,
            instance_id=self.owner,
            model_repository_id=self.uuid,
        )


class ModelRpositoriesClient(BaseResourcesClient):
    """
    Client for Model Repositories resource of AFS v2 API.
    """

    def __init__(self, afs_client, instance_id, *args, **kwargs):
        api_resource = "model_repositories"
        api_path = "{}/instances/{}/{}".format(
            afs_client.api_version, instance_id, api_resource
        )
        super().__init__(
            afs_client=afs_client,
            api_resource=api_resource,
            api_path=api_path,
            resource_model=ModelRepository,
            exception=ModelRepositoriesClientError,
            *args,
            **kwargs
        )
