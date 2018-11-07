import pkg_resources
import requests
import warnings
from urllib.parse import urljoin
import os

# afs-sdk module
from .config_handler import config_handler
from .flow import flow
from .models import models
from .services import services

if requests.__version__ < '2.18.3':
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
else:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__version__ = pkg_resources.get_distribution('afs').version

def _check_version(__version__):
    target_endpoint = os.getenv('afs_url', None)

    if target_endpoint is not None:

        if not target_endpoint.startswith(('http://', 'https://')):
            target_endpoint = 'https://' + target_endpoint

        resp = requests.get(
            urljoin(target_endpoint, 'info'), verify=False
        )

        if not resp.ok:
            message = {
                'error': 'Get info from {0} failed'.format(target_endpoint),
                'response': resp.text
            }
            raise Exception(message)

        resp = resp.json()
        afs_version = resp['AFS_version']
        if afs_version != __version__:
            warnings.warn('SDK version is {0}, and AFS platform version is {1}. It will cause some compatibility issues.'.format(__version__, afs_version))
    else:
        warnings.warn('User environment is not on AFS.')

_check_version(__version__)
