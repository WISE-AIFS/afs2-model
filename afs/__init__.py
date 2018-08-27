import pkg_resources
import urllib3

from .config_handler import config_handler
from .flow import flow
from .models import models
from .services import services

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__version__ = pkg_resources.get_distribution('afs').version
__all__ = [
    'models', 'config_handler', 'services'
]
