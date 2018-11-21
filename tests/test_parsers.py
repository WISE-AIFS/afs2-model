import json
import os
import shutil

import pytest

import git
from afs.parsers import manifest_parser, node_config_parser


@pytest.mark.skip(reason='Can not access GitLab')
def test_manifest_parser_API():
    git_username = os.getenv('git_username', '')
    git_password = os.getenv('git_password', '')
    git_url = os.getenv('git_url', '')
    pypi_endpoint = os.getenv('pypi_endpoint', '')
    # with open('../VERSION', 'r') as f:
    #     afs_sdk_version=f.read()
    afs_sdk_version='1.2.29.dev3'
    # afs_sdk_version=None

    if not os.path.exists('test_workspace'):
        os.mkdir('test_workspace')
        git.Repo.clone_from(url=git_url.format(git_username, git_password),
                                   to_path='./test_workspace')

    ipynb_name = next(iter([filename for filename in os.listdir(os.path.join('test_workspace', 'src'))
                            if filename.endswith('.ipynb')]), None)

    ipynb_path = os.path.join('test_workspace', 'src', ipynb_name)
    manifest_parser(ipynb_path, output_dir='test_workspace/src',
                    pypi_endpoint=pypi_endpoint, manifest_yaml=False, afs_sdk_version=afs_sdk_version)

    assert 'manifest.json' in os.listdir(os.path.join('test_workspace', 'src'))
    assert 'requirements.txt' in os.listdir(os.path.join('test_workspace', 'src'))
    assert 'runtime.txt' in os.listdir(os.path.join('test_workspace', 'src'))
    assert 'startup.sh' in os.listdir(os.path.join('test_workspace' ,'src'))

    with open(os.path.join('test_workspace', 'src', 'manifest.json'), 'r') as f:
        manifest_contents = json.loads(f.read())
    assert manifest_contents.get('name') != None
    assert manifest_contents.get('type') == 'API'
    assert manifest_contents.get('command') == 'sh startup.sh'

    # shutil.rmtree('test_workspace')

def test_node_config_parser():
    pass
