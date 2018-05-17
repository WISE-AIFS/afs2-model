"""
    This module provides a client library for afs.
"""

__version__ = "1.2.1"
from .models import models
from .config_handler import config_handler
from .flow import flow

__all__ = [
    'models', 'config_handler'
]
