import json
import os
from afs.parsers import manifest_parser, node_config_parser
from pathlib import Path


def test_manifest_parser_API():
    pypi_endpoint = os.getenv('pypi_endpoint', '')
    afs_sdk_version='1.3.0'

    if not os.path.exists('test_workspace'):
        os.mkdir('test_workspace')

    ipynb_path = os.path.join(Path(__file__).parent, 'data', 'iii_Dt.ipynb')

    manifest_parser(ipynb_path, output_dir='test_workspace',
                    pypi_endpoint=pypi_endpoint, manifest_yaml=False, afs_sdk_version=afs_sdk_version)

    assert 'manifest.json' in os.listdir(os.path.join('test_workspace'))
    assert 'requirements.txt' in os.listdir(os.path.join('test_workspace'))
    assert 'runtime.txt' in os.listdir(os.path.join('test_workspace'))
    assert 'startup.sh' in os.listdir(os.path.join('test_workspace'))

    with open(os.path.join('test_workspace', 'manifest.json'), 'r') as f:
        manifest_contents = json.loads(f.read())
    assert manifest_contents.get('name') != None
    assert manifest_contents.get('type') == 'API'
    assert manifest_contents.get('command') == 'sh startup.sh'

    with open(os.path.join('test_workspace', 'requirements.txt'), 'r') as f:
        afs_req = next(iter([req for req in f.read().split('\n') if req.startswith('afs')]), None)
        assert afs_req == 'afs==1.2.27'

    # shutil.rmtree('test_workspace')

def test_node_config_parser():
    pass
