"""
    This module provides a client library for afs.
"""

__version__ = "1.1.4"
from .models import models
from .config_handler import config_handler


__all__ = [
    'models', 'config_handler'
]
