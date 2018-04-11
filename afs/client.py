from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from afs.models import models
import os
import json

_logger = logging.getLogger(__name__)


class afs():
    def __init__(self, target_endpoint=None, instance_id=None, auth_code=None):
        self.target_endpoint = os.getenv('afs_url', None)
        self.auth_code = os.getenv('auth_code', None)
        vcap = json.loads(os.getenv('VCAP_APPLICATION', {}))
        if not vcap:
            raise AssertionError('Environment VCAP_APPLICATION is empty')
        self.instance_id = vcap.get('space_name', None)

        if self.target_endpoint == None or self.instance_id == None or self.auth_code == None:
            raise AssertionError('Environment parameters need afs_url, instance_id, auth_code')

        if not self.target_endpoint.endswith('/'):
            self.target_endpoint = self.target_endpoint + '/'
        self.target_endpoint = self.target_endpoint + 'v1/'

        self.models = models(self.target_endpoint, self.instance_id, self.auth_code)

    @classmethod
    def create(self, target_endpoint , instance_id, auth_code):
        self.target_endpoint = target_endpoint
        self.auth_code = auth_code
        self.instance_id = instance_id

        if not self.target_endpoint.endswith('/'):
            self.target_endpoint = self.target_endpoint + '/'
        self.target_endpoint = self.target_endpoint + 'v1/'

        self.models = models(self.target_endpoint, self.instance_id, self.auth_code)

