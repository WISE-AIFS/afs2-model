from afs.parsers import manifest_parser, node_config_parser
import git
import os
import shutil
import json

def test_manifest_parser_API():
    username=os.getenv('git_username', '')
    password=os.getenv('git_password', '')

    if not os.path.exists('test_workspace'):
        os.mkdir('test_workspace')
        git.Repo.clone_from(url='https://{}:{}@gitlab.iii-cflab.com/iii/iii_dt.git'.format(username, password),
                                   to_path='./test_workspace')

    ipynb_name = next(iter([filename for filename in os.listdir(os.path.join('test_workspace', 'src'))
                            if filename.endswith('.ipynb')]), None)

    ipynb_path = os.path.join('test_workspace', 'src', ipynb_name)
    manifest_parser(ipynb_path, output_dir='test_workspace/src', pypi_endpoint=None, manifest_yaml=False)

    assert 'manifest.json' in os.listdir(os.path.join('test_workspace/src'))
    assert 'requirements.txt' in os.listdir(os.path.join('test_workspace/src'))
    assert 'runtime.txt' in os.listdir(os.path.join('test_workspace/src'))
    assert 'startup.sh' in os.listdir(os.path.join('test_workspace/src'))

    with open(os.path.join('test_workspace', 'src', 'manifest.json'), 'r') as f:
        manifest_contents = json.loads(f.read())
    assert manifest_contents.get('name') != None
    assert manifest_contents.get('type') == 'API'
    assert manifest_contents.get('command') == 'sh startup.sh'

    # shutil.rmtree('test_workspace')

def test_node_config_parser():
    pass