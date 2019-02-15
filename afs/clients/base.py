from abc import ABC
from urllib.parse import urljoin

from requests import Response

from .exceptions import AFSClientError, APIRequestError, APIResponseError


class APISession:
    """
    Default API session with timeout and retry
    """
    def __init__(self, session=None, timeout: int = 5, retry: int = 3, *args, **kwargs):
        self.timeout = timeout
        self.retry = retry

        if not session:
            # TODO: Support aiohttp
            from requests import Session
            session = Session(*args, **kwargs)

        self._session = session

    def __getattr__(self, attr):
        return getattr(self._session, attr)

    def request(self, raw=False, *args, **kwargs):
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        retry = self.retry
        while retry > 0:
            try:
                resp = self._session.request(*args, **kwargs)
            except Exception as e:
                retry -= 1
                if retry == 0:
                    raise APIRequestError(e)
            else:
                break

        if not raw:
            resp = APIResponse(resp)
        return resp

    def get(self, url, *args, **kwargs):
        return self.request(method='get', url=url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self.request(method='post', url=url, *args, **kwargs)

    def put(self, url, *args, **kwargs):
        return self.request(method='put', url=url, *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        return self.request(method='delete', url=url, *args, **kwargs)

    def patch(self, url, *args, **kwargs):
        return self.request(method='patch', url=url, *args, **kwargs)

    def head(self, url, *args, **kwargs):
        return self.request(method='head', url=url, *args, **kwargs)

    def options(self, url, *args, **kwargs):
        return self.request(method='options', url=url, *args, **kwargs)


class APIResponse(dict, Response):

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
            for key, value in self._to_json().items():
                self[key] = value

    def __getattr__(self, attr):
        return getattr(self._raw_response, attr)

    def _to_json(self):
        try:
            resp = self._raw_response.json()
        except Exception:
            raise APIResponseError('Invalid JSON response: {}'.format(self._raw_response.text))

        return resp


class BaseResourceModel(dict, object):
    """
    The base class for all resource model
    """

    def __init__(self, resource_client, api_endpoint, resource=None, json_loads=None, json_dumps=None, *args, **kwargs):
        super().__init__(kwargs)

        self._resource_client = resource_client
        self.resource = resource or 'base'
        self.api_endpoint = api_endpoint

        if not json_loads:
            from json import loads as json_loads
        self.json_loads = json_loads

        if not json_dumps:
            from json import dumps as json_dumps
        self.json_dumps = json_dumps

    def __getattr__(self, attr):
        return self[attr]

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

    def __init__(self, afs_client, resource, path, resource_model, exception=None):
        self._afs_client = afs_client
        self.api_resource = resource
        self.api_path = path
        self.api_endpoint = urljoin(
            self._afs_client.api_endpoint, self.api_path
        )
        self.resource_model = resource_model or BaseResourceModel
        self.exception = exception or AFSClientError

    def __call__(self, uuid=None, start=0, limit=10, **kwargs):
        """
        List all resources.
        """

        if uuid:
            return self.get(uuid=uuid)

        kwargs.update({
            'start': start,
            'limit': limit
        })

        try:
            resp = self._afs_client.session.get(
                self.api_endpoint,
                params=kwargs
            )
        except NotImplementedError:
            raise NotImplementedError('List not support for resource: {}'.format(self.api_resource))
        except Exception as e:
            raise self.exception(e)

        resources = resp.get('resources')
        if resources is None:
            raise self.exception('List all {} failed'.format(self.api_resource))

        pagination = resp.get('pagination')
        self.total = pagination.get('total', len(resources))

        resources = [
            self.resource_model(
                resource_client=self,
                api_endpoint='{}/{}'.format(self.api_endpoint, resource['uuid']),
                **resource) for resource in resources
        ]
        return resources

    def get(self, uuid, **kwargs):
        """
        Get a resource by uuid.
        """

        raw = kwargs.pop('raw', False)

        url = urljoin(
            self._afs_client.api_endpoint, '{}/{}'.format(self.api_path, uuid)
        )

        try:
            resp = self._afs_client.session.get(
                url,
                params=kwargs,
                raw=raw
            )
        except NotImplementedError:
            raise NotImplementedError('Get not support for resource {}'.format(self.api_resource))
        except Exception as e:
            raise self.exception(e)

        if raw:
            return resp
        return self.resource_model(resource_client=self, api_endpoint=url, **resp)

    def create(self, **kwargs):
        """
        Create a new resource.
        """
        try:
            resp = self._afs_client.session.post(
                self.api_endpoint,
                json=kwargs
            )
        except NotImplementedError:
            raise NotImplementedError('Create not support for resource {}'.format(self.api_resource))
        except Exception as e:
            raise self.exception(e)

        return self.resource_model(
            resource_client=self,
            api_endpoint='{}/{}'.format(self.api_endpoint, resp['uuid']),
            **resp)

    def update(self, uuid, **kwargs):
        """
        Update a resource.
        """

        url = urljoin(
            self._afs_client.api_endpoint, '{}/{}'.format(self.api_path, uuid)
        )

        try:
            resp = self._afs_client.session.put(url)
        except NotImplementedError:
            raise NotImplementedError('Update not support for resource {}'.format(self.api_resource))
        except Exception as e:
            raise self.exception(e)

        return self.resource_model(resource_client=self, api_endpoint=url, **resp)

    def delete(self, uuid):
        """
        Delete a resource.
        """

        url = urljoin(
            self._afs_client.api_endpoint, '{}/{}'.format(self.api_path, uuid)
        )

        try:
            resp = self._afs_client.session.delete(url)
        except NotImplementedError:
            raise NotImplementedError('Delete not support for resource {}'.format(self.api_resource))
        except Exception as e:
            raise self.exception(e)

        return {}
        # return self.resource_model(resource_client=self, api_endpoint=url, **resp)
