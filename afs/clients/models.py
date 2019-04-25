from .base import BaseResourceModel, BaseResourcesClient
from .exceptions import ModelsClientError


class Model(BaseResourceModel):
    """
    Resource model for Models resource of AFS v2 API.
    """

    def __init__(self, resource_client, *args, **kwargs):
        resource = "model"
        super().__init__(
            resource_client=resource_client, resource=resource, *args, **kwargs
        )

    @property
    def binary(self):
        return self._resource_client.get(self.uuid, alt="media", raw=True).content

    def download(self, model_path):
        with open(model_path, "wb") as f:
            f.write(self.binary)
        return True


class ModelsClient(BaseResourcesClient):
    """
    Client for Models resource of AFS v2 API.
    """

    def __init__(self, afs_client, instance_id, model_repository_id, *args, **kwargs):
        api_resource = "models"
        api_path = "{api_version}/instances/{instance_id}/model_repositories/{model_repository_id}/{api_resource}".format(
            api_version=afs_client.api_version,
            instance_id=instance_id,
            model_repository_id=model_repository_id,
            api_resource=api_resource,
        )
        super().__init__(
            afs_client=afs_client,
            api_resource=api_resource,
            api_path=api_path,
            resource_model=Model,
            exception=ModelsClientError,
            *args,
            **kwargs
        )

    def create(self, json_dumps=None, **kwargs):
        """
        Create a new model.

        :param str model_path: Path to the model file.
        :param str name: The name of model.
        :return: The response of created model.
        :rtype: Model
        """
        model_path = kwargs.pop("model_path", None)
        if not model_path:
            raise ModelsClientError("Invalid model_path")

        if not json_dumps:
            from json import dumps as json_dumps

        attrs = ["evaluation_result", "parameters", "tags"]

        for attr in attrs:
            value = kwargs.pop(attr, None)
            if value:
                if isinstance(value, dict):
                    kwargs[attr] = json_dumps(value)
                elif isinstance(value, str):
                    kwargs[attr] = value

        try:
            resp = self._afs_client._session.post(
                self.api_endpoint, files={"model": open(model_path, "rb")}, data=kwargs
            )
        except Exception as e:
            raise self.exception(e)

        return self.resource_model(
            resource_client=self,
            api_endpoint="{}/{}".format(self.api_endpoint, resp["uuid"]),
            **resp
        )
