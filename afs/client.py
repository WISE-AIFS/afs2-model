import logging
from afs.models import models
import os
import json

_logger = logging.getLogger(__name__)

class afs():
    def __init__(self):
        self.target_endpoint = os.getenv('afs_url', None)
        self.auth_code = os.getenv('auth_code', None)
        vcap = json.loads(os.getenv('VCAP_APPLICATION', {}))
        if vcap is {}:
            raise AssertionError('Environment VCAP_APPLICATION is empty')
        self.instance_id = vcap.get('space_name', None)

        if self.target_endpoint == None or self.instance_id == None or self.auth_code == None:
            raise AssertionError('Environment parameters need afs_url, instance_id, auth_code')

        self.models = models(self.target_endpoint, self.instance_id, self.auth_code, 'models')

if __name__ == '__main__':
    client = afs()
    print(client.models.upload_model('__init__.py', accuracy=0.4, loss=0.3, tags=dict(qwe='qwe'), extra_evaluation=dict(qwe='qwe')) )
