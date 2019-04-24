import pkg_resources
import requests

# afs-sdk module
from .models import models

if requests.__version__ < '2.18.3':
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
else:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__version__ = pkg_resources.get_distribution('advantech-afs').version
