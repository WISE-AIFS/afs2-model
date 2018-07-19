"""
    This module provides a client library for afs.
"""
import os

import pkg_resources

from .config_handler import config_handler
from .flow import flow
from .models import models

__version__ = pkg_resources.get_distribution('afs').version
__all__ = [
    'models', 'config_handler'
]
