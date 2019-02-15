import pkg_resources

from .clients import AFSClient

__version__ = pkg_resources.get_distribution('afs').version
