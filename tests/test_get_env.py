import os
from tests.mock_requests import MockResponse


def test_info_v2_check(test_env):
    from afs.get_env import AfsEnv

    afs_env = AfsEnv()
    assert afs_env.afs_url == os.getenv("afs_url", None)
    assert afs_env.instance_id == os.getenv("instance_id", None)
    assert afs_env.target_endpoint == "{}/v2/".format(os.getenv('afs_url', None) )
    assert afs_env.bucket_name != None
    assert afs_env.version != None
