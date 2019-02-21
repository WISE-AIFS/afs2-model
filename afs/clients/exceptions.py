class APIRequestError(IOError):
    """
    Default exception for APISession.
    """
    pass


class APIResponseError(IOError):
    """
    Default exception for APIResponse.
    """
    pass


class AFSClientError(Exception):
    """
    Default exception for AFS Client.
    """
    pass


class SSOClientError(Exception):
    """
    Default exception for SSO Client.
    """
    pass


class InstancesClientError(Exception):
    """
    Default exception for Instance resource.
    """
    pass


class ModelRepositoriesClientError(Exception):
    """
    Default exception for Model Repository resource.
    """
    pass


class ModelsClientError(Exception):
    """
    Default exception for Model resource.
    """
    pass
