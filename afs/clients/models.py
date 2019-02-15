from .base import BaseResourceModel, BaseResourcesClient
from .exceptions import ModelsClientError


class Model(BaseResourceModel):
    """
    Resource model for Models resource of AFS v2 API.
    """

    def __init__(self, resource_client, *args, **kwargs):
        resource = 'model'
        super().__init__(resource_client=resource_client, resource=resource, *args, **kwargs)


class ModelsClient(BaseResourcesClient):
    """
    Client for Models resource of AFS v2 API.
    """

    def __init__(self, afs_client, instance_id, model_repository_id, *args, **kwargs):
        resource = 'models'
        path = '{api_version}/instances/{instance_id}/model_repositories/{model_repository_id}/{resource}'.format(
            api_version=afs_client.api_version,
            instance_id=instance_id,
            model_repository_id=model_repository_id,
            resource=resource)
        super().__init__(
            afs_client=afs_client,
            resource=resource,
            path=path,
            resource_model=Model,
            exception=ModelsClientError,
            *args,
            **kwargs)

    def create(self, json_dumps=None, **kwargs):
        """
        Create a new model.

        :param str model_path: Path to the model file.
        :param str name: The name of model
        :return: 
        """
        model_path = kwargs.pop('model_path', None)
        if not model_path:
            raise ModelsClientError('Invalid model_path')

        if not json_dumps:
            from json import dumps as json_dumps

        if 'evaluation_result' in kwargs:
            kwargs['evaluation_result'] = json_dumps(kwargs['evaluation_result'])

        if 'parameters' in kwargs:
            kwargs['parameters'] = json_dumps(kwargs['parameters'])

        if 'tags' in kwargs:
            kwargs['tags'] = json_dumps(kwargs['tags'])

        try:
            resp = self._afs_client.session.post(
                self.api_endpoint,
                files={'model': open(model_path, 'rb')},
                data=kwargs
            )
        except Exception as e:
            raise self.exception(e)

        return self.resource_model(
            resource_client=self,
            api_endpoint='{}/{}'.format(self.api_endpoint, resp['uuid']),
            **resp)
