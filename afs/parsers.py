import os
import ast
import json
from pathlib import Path
import yaml

JUPYTER_RUNTIME = 'python-3.6.x'
JUPYTER_DEFAULT_DISK = 2048
with open(Path(__file__).parent.joinpath('template', 'jupyter_app_default_requirements.txt'), 'r') as f:
    JUPYTER_APP_DEFAULT_REQUIREMENTS = f.read()

with open(Path(__file__).parent.joinpath('template', 'jupyter_api_default_requirements.txt'), 'r') as f:
    JUPYTER_API_DEFAULT_REQUIREMENTS = f.read()
JUPYTER_APP_DEFAULT_COMMAND = 'bash'
JUPYTER_API_DEFAULT_COMMAND = 'sh startup.sh'
JUPYTER_API_STARTUP = """
#!/bin/bash

# Disable SQLite history
mkdir -p /home/vcap/app/.ipython/profile_default
cat << EOF > /home/vcap/app/.ipython/profile_default/ipython_kernel_config.py
# Configuration file for ipython-kernel.
c = get_config()
c.HistoryManager.enabled = False
EOF

# Jupyter kernel gateway configs
mkdir -p /home/vcap/app/.jupyter
cat << EOF > /home/vcap/app/.jupyter/jupyter_kernel_gateway_config.py
# Configuration file for jupyter-kernel-gateway.
c.KernelGatewayApp.seed_uri='{notebook_name}'
c.KernelGatewayApp.prespawn_count=5
c.KernelGatewayApp.api='notebook-http'
c.KernelGatewayApp.ip='0.0.0.0'
c.KernelGatewayApp.port=$PORT
c.NotebookHTTPPersonality.static_path='./static'
EOF

jupyter-kernelgateway
"""


def manifest_parser(notebook_path, pypi_endpoint, output_dir=None, manifest_yaml=False, afs_sdk_version=None):
    """
    The method parses the manifest in notebook, including  manifest.json, requirements.txt, runtime.txt, startup.sh.
    :param str notebook_path: the path of notebook (.ipynb) will be parsed.
    :param str pypi_endpoint: the requirement would be specific pypi server
    :param str output_dir: the files would be output in specific path. Default is current directory
    :param bool manifest_yaml: write manifest.yml or not
    :param str afs_sdk_version: parse manifest to specific afs sdk version requirement
    :rtype: True or logger message
    """
    if not os.path.exists(notebook_path):
        raise FileNotFoundError

    if not notebook_path.endswith('.ipynb'):
        raise ValueError('The file name extension is not ipynb.')

    if output_dir is None:
        output_dir = '.'
    else:
        if not os.path.isdir(output_dir):
            raise NotADirectoryError('{} is not a directory'.format(output_dir))

    with open(notebook_path, 'r') as f:
        notebook_content = json.loads(f.read())

    manifest = next(
        (notebook_content['cells'][0]['source']
         for index, cell in enumerate(notebook_content['cells'])
         if index == 0 and ''.join(cell['source']).replace('\n', '').startswith('manifest')), '')
    manifest = ''.join(manifest).replace('\n', '')
    manifest = config_to_dict(manifest, 'manifest') if manifest else {}

    disk_quota = manifest.get('disk_quota', 0)
    if isinstance(disk_quota, str):
        unit = 1
        if disk_quota.endswith(('M', 'MB')):
            unit = 1
        elif disk_quota.endswith(('G', 'GB')):
            unit = 1024
        disk_quota = int(''.join(filter(str.isdigit, disk_quota))) * unit

    # Force use 2G disk
    if disk_quota < 2048:
        manifest.update({'disk_quota': 2048})

    analytic_app_type = manifest.get('type', 'APP')
    if not analytic_app_type == 'APP' and not analytic_app_type == 'API':
        analytic_app_type = 'APP'

    command = manifest.get('command', JUPYTER_API_DEFAULT_COMMAND if analytic_app_type == 'API' else JUPYTER_APP_DEFAULT_COMMAND)
    notebook_name = notebook_path.split(os.path.sep)[-1]

    # Generate auto run command
    if manifest.get('auto_run') and analytic_app_type == 'APP':
        command = 'run_jnb {0} -m false'.format(notebook_name)

    buildpack = 'python_buildpack_offline'
    requirements = JUPYTER_APP_DEFAULT_REQUIREMENTS if analytic_app_type == 'APP' else JUPYTER_API_DEFAULT_REQUIREMENTS
    req_list = [ req.split('==')[0] for req in requirements.split('\n')]

    # Generate requirements.txt
    pypi_host = pypi_endpoint.replace('https://', '').replace('http://', '').split(':')[0]
    requirements = '--index-url {0}\n--trusted-host {1}\n'.format(pypi_endpoint, pypi_host) + requirements

    if 'requirements' in manifest:
        requirements_append = [req for req in manifest['requirements'] if req not in req_list]

        if afs_sdk_version:
            add_new_version = False
            for afs_req in [req for req in requirements_append if req=='afs']:
                add_new_version = True
                requirements_append.remove(afs_req)
            if add_new_version:
                requirements_append.append('afs=={}'.format(afs_sdk_version))

        requirements = requirements + '\n'.join(requirements_append)

    data = {}
    data['name'] = notebook_name.split('.')[0]
    data['command'] = command
    data['memory'] =  int(manifest['memory']) if manifest.get('memory') else None
    data['buildpack'] = buildpack
    data['disk_quota'] = int(manifest['disk_quota']) if manifest.get('disk_quota') else None

    if analytic_app_type == 'APP':
        data['type'] = 'APP'
        data['health_check_type'] = 'process'
    else:
        data['type'] = 'API'
        data['health_check_type'] = 'port'
        startup_mapping = {
            'notebook_name': notebook_name,
        }
        with open(os.path.join(output_dir, 'startup.sh'), 'w') as f:
            f.write(JUPYTER_API_STARTUP.format_map(startup_mapping))

    if manifest_yaml:
        manifest_yml={
            'applications':[
                {'name': data['name'],
                 'command': data['command'],
                 'memory': str(data['memory'])+'MB',
                 'disk_quota': str(data['disk_quota'])+'MB',
                 'buildpack': data['buildpack'],
                 'type': data['type'],
                 }
            ]
        }
        with open(os.path.join(output_dir, 'manifest.yml'), 'w') as f:
            yaml.dump(manifest_yml, f, default_flow_style=False)

    with open(os.path.join(output_dir, 'requirements.txt'), 'w') as f:
        f.write(requirements)

    with open(os.path.join(output_dir, 'manifest.json'), 'w') as f:
        f.write(json.dumps(data))

    with open(os.path.join(output_dir, 'runtime.txt'), 'w') as f:
        f.write(JUPYTER_RUNTIME)

    return True



def node_config_parser():
    pass



def config_to_dict(source, startswith='node_config'):
    """
    Transform config(manifest or node_config) from jupyter source code to python dict.

    :param str source: config source code in jupyter.
    :return config: transform config from source code to dictionary.
    :rtypr: dict
    """
    if source.startswith(startswith, None):
        config = '{' + '{'.join(source.split('{')[1:])
    else:
        config = source

    try:
        config = json.loads(config)
    except ValueError:
        try:
            config = ast.literal_eval(config)
        except SyntaxError as e:
            raise RuntimeError('Failed to parse notebook.')

    return config
