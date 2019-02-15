from .base import BaseResourceModel, BaseResourcesClient
from .exceptions import InstancesClientError
from .mode_repositories import ModelRpositoriesClient


class Instance(BaseResourceModel):
    def __init__(self, resource_client, *args, **kwargs):
        resource = 'instance'
        super().__init__(resource_client=resource_client, resource=resource, *args, **kwargs)
        self.model_repositories = ModelRpositoriesClient(afs_client=resource_client._afs_client, instance_id=self.uuid)


class InstancesClient(BaseResourcesClient):
    def __init__(self, afs_client, *args, **kwargs):
        resource = 'instances'
        path = '{}/{}'.format(afs_client.api_version, resource)
        super().__init__(
            afs_client=afs_client,
            resource=resource,
            path=path,
            resource_model=Instance,
            exception=InstancesClientError,
            *args,
            **kwargs)
