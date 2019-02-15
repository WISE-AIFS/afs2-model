class APIRequestError(IOError):
    pass


class APIResponseError(IOError):
    pass


class AFSClientError(Exception):
    pass


class SSOException(Exception):
    pass


class InstancesClientError(Exception):
    pass


class ModelRepositoriesClientError(Exception):
    pass


class ModelsClientError(Exception):
    pass
