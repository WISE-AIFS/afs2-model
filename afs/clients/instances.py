from .base import BaseResourceModel, BaseResourcesClient
from .exceptions import InstancesClientError
from .model_repositories import ModelRpositoriesClient


class Instance(BaseResourceModel):
    """
    Resource model for Instance resource of AFS v2 API.
    """
    def __init__(self, resource_client, *args, **kwargs):
        resource = 'instance'
        super().__init__(
            resource_client=resource_client,
            resource=resource,
            *args,
            **kwargs
        )

        # Add sub-resource client if needed
        self.model_repositories = ModelRpositoriesClient(
            afs_client=resource_client._afs_client,
            instance_id=self.uuid
        )


class InstancesClient(BaseResourcesClient):
    """
    Client for Instance resource of AFS v2 API.
    """
    def __init__(self, afs_client, *args, **kwargs):
        api_resource = 'instances'
        api_path = '{}/{}'.format(afs_client.api_version, api_resource)
        super().__init__(
            afs_client=afs_client,
            api_resource=api_resource,
            api_path=api_path,
            resource_model=Instance,
            exception=InstancesClientError,
            *args,
            **kwargs
        )
