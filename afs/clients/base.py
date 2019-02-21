from abc import ABC
from urllib.parse import urljoin

from requests import Response, Session
from requests.adapters import HTTPAdapter

from .exceptions import AFSClientError, APIRequestError, APIResponseError


# TODO: Support aiohttp
class APISession(Session):
    """
    Default API session with timeout and retry
    """

    def __init__(
            self,
            timeout: int = 7,
            retry: int = 3,
            token=None,
            ssl=True,
            *args,
            **kwargs
    ):
        self.timeout = timeout
        self.retry = retry
        self.token = token
        self.auto_refresh_token = True if self.token else False

        super().__init__(*args, **kwargs)
        self.mount(prefix='*', adapter=HTTPAdapter(max_retries=self.retry))
        self.verify = ssl

    def request(self, *args, **kwargs):
        raw = kwargs.pop('raw', None)
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        retry = self.retry
        while retry > 0:
            try:
                resp = super().request(*args, **kwargs)
            except Exception as e:
                retry -= 1

                if retry == 0:
                    raise APIRequestError(e)

            else:
                # Auto refresh token
                if resp.status_code == 401 and self.auto_refresh_token:
                    self.token = self.refresh_token(self.token)
                    self.headers.update(
                        {'Authorization': 'Bearer {}'.format(self.token)}
                    )
                    continue

                else:
                    break

        if not raw:
            resp = APIResponse(resp)
        return resp

    def enable_auto_refresh_token(self, token, refresh_token_func):
        """
        Enable auto refresh. After enable auto refresh, this session will use 
        self.refresh_token update self.token if there is any 401 response happened.

        :param str token: The token of this session.
        :param func refresh_token_func: The function used to refresh token.
        """
        self.token = token
        self.auto_refresh_token = True
        self.refresh_token = refresh_token_func


class APIResponse(dict):
    def __init__(self, response):
        try:
            response.raise_for_status()
        except Exception as e:
            if response.status_code == 405:
                raise NotImplementedError
            raise APIResponseError(response.text or e)

        self._raw_response = response
        if not self._raw_response.content and self._raw_response.status_code == 204:
            self = None
        else:
            super().__init__(**self.to_dict())

    def to_dict(self):
        try:
            resp = self._raw_response.json()
        except Exception:
            raise APIResponseError(
                'Invalid JSON response: {}'.format(self._raw_response.text)
            )

        return resp


class BaseResourceModel(dict):
    """
    The base class for all resource model
    """

    def __init__(
            self,
            resource_client,
            api_endpoint,
            resource=None,
            json_loads=None,
            json_dumps=None,
            *args,
            **kwargs
    ):
        super().__init__(kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._resource_client = resource_client
        self.resource = resource or 'base'
        self.api_endpoint = api_endpoint

        if not json_loads:
            from json import loads as json_loads
        self.json_loads = json_loads

        if not json_dumps:
            from json import dumps as json_dumps
        self.json_dumps = json_dumps

    def loads(self, json_string):
        """
        Load json into attributes.
        """
        for key, value in self.json_loads(json_string).items():
            self[key] = value

    def dumps(self):
        """
        Dump attributes to JSON string.
        """
        return self.json_dumps(self)

    def update(self, **kwargs):
        return self._resource_client.update(uuid=self.uuid, **kwargs)

    def delete(self):
        return self._resource_client.delete(uuid=self.uuid)


class BaseResourcesClient():
    """
    The base resource class for all clients.
    """

    def __init__(
            self,
            afs_client,
            api_resource,
            api_path,
            resource_model,
            exception=None
    ):
        self._afs_client = afs_client
        self.api_resource = api_resource
        self.api_path = api_path
        self.api_endpoint = urljoin(
            self._afs_client.api_endpoint,
            self.api_path
        )
        self.resource_model = resource_model or BaseResourceModel
        self.exception = exception or AFSClientError

    def __call__(self, uuid=None, start=0, limit=10, **kwargs):
        """
        List all resources.
        """

        if uuid:
            return self.get(uuid=uuid)

        kwargs.update({'start': start, 'limit': limit})

        try:
            resp = self._afs_client._session.get(
                self.api_endpoint,
                params=kwargs
            )
        except NotImplementedError:
            raise NotImplementedError(
                'List not support for resource: {}'.format(self.api_resource)
            )
        except Exception as e:
            raise self.exception(e)

        resources = resp.get('resources')
        if resources is None:
            raise self.exception(
                'List all {} failed'.format(self.api_resource)
            )

        pagination = resp.get('pagination')
        self.total = pagination.get('total', len(resources))

        resources = [
            self.resource_model(
                resource_client=self,
                api_endpoint='{}/{}'.format(
                    self.api_endpoint,
                    resource['uuid']
                ),
                **resource
            ) for resource in resources
        ]
        return resources

    def get(self, uuid, **kwargs):
        """
        Get a resource by uuid.
        """

        raw = kwargs.pop('raw', False)

        url = '{}/{}'.format(self.api_endpoint, uuid)

        try:
            resp = self._afs_client._session.get(url, params=kwargs, raw=raw)
        except NotImplementedError:
            raise NotImplementedError(
                'Get not support for resource {}'.format(self.api_resource)
            )
        except Exception as e:
            raise self.exception(e)

        if raw:
            return resp
        return self.resource_model(
            resource_client=self,
            api_endpoint=url,
            **resp.to_dict()
        )

    def create(self, **kwargs):
        """
        Create a new resource.
        """
        try:
            resp = self._afs_client._session.post(
                self.api_endpoint,
                json=kwargs
            )
        except NotImplementedError:
            raise NotImplementedError(
                'Create not support for resource {}'.format(self.api_resource)
            )
        except Exception as e:
            raise self.exception(e)

        return self.resource_model(
            resource_client=self,
            api_endpoint='{}/{}'.format(self.api_endpoint,
                                        resp['uuid']),
            **resp.to_dict()
        )

    def update(self, uuid, **kwargs):
        """
        Update a resource.
        """

        url = '{}/{}'.format(self.api_endpoint, uuid)

        try:
            resp = self._afs_client._session.put(url)
        except NotImplementedError:
            raise NotImplementedError(
                'Update not support for resource {}'.format(self.api_resource)
            )
        except Exception as e:
            raise self.exception(e)

        return self.resource_model(
            resource_client=self,
            api_endpoint=url,
            **resp.to_dict()
        )

    def delete(self, uuid):
        """
        Delete a resource.
        """

        url = '{}/{}'.format(self.api_endpoint, uuid)

        try:
            resp = self._afs_client._session.delete(url)
        except NotImplementedError:
            raise NotImplementedError(
                'Delete not support for resource {}'.format(self.api_resource)
            )
        except Exception as e:
            raise self.exception(e)

        return {}
