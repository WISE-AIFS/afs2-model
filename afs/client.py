import logging
from afs.models import models
import os

_logger = logging.getLogger(__name__)

class afs():
    def __init__(self):
        # self.target_endpoint = os.getenv('afs_url', None)
        # self.instance_id = json.loads(os.environ['VCAP_APPLICATION'],dict(space_name={})).get('space_name', None)
        # self.auth_code = os.getenv('auth_code', None)

        self.target_endpoint = os.getenv('afs_url', 'http://portal-afs-develop.iii-cflab.com/v1/')
        self.instance_id = os.getenv('VCAP_APPLICATION',dict(space_name='5ba61762-f5f0-47b4-9769-9e1756ebf0c5')).get('space_name', None)
        self.auth_code = os.getenv('auth_code', 'ZGeZHz68Byuzw1O5ZFx-_A')
        if self.target_endpoint == None or self.instance_id == None or self.auth_code == None:
            raise AssertionError('Environment parameters need afs_url, instance_id, auth_code')
        self.models = models(self.target_endpoint, self.instance_id, self.auth_code, 'models')

if __name__ == '__main__':
    client = afs()
    print(client.models.upload_model('__init__.py', accuracy=0.4, loss=0.3, tags=dict(qwe='qwe'), extra_evaluation=dict(qwe='qwe')) )
