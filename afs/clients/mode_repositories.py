from .base import BaseResourceModel, BaseResourcesClient
from .exceptions import ModelRepositoriesClientError
from .models import ModelsClient


class ModelRepository(BaseResourceModel):
    """
    Resource model for Model Repositories resource of AFS v2 API.
    """

    def __init__(self, resource_client, *args, **kwargs):
        resource = 'model_erpository'
        super().__init__(resource_client=resource_client, resource=resource, *args, **kwargs)
        self.models = ModelsClient(resource_client._afs_client, instance_id=self.owner, model_repository_id=self.uuid)


class ModelRpositoriesClient(BaseResourcesClient):
    """
    Client for Model Repositories resource of AFS v2 API.
    """

    def __init__(self, afs_client, instance_id, *args, **kwargs):
        resource = 'model_repositories'
        path = '{}/instances/{}/{}'.format(afs_client.api_version, instance_id, resource)
        super().__init__(
            afs_client=afs_client,
            resource=resource,
            path=path,
            resource_model=ModelRepository,
            exception=ModelRepositoriesClientError,
            *args,
            **kwargs)
