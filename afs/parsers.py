import os
import ujson
import ast
import logger
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


def manifest_parser(notebook_path, output_dir=None):
    if not os.path.exists(notebook_path):
        raise FileNotFoundError

    if output_dir is None:
        output_dir = '.'

    with open(notebook_path, 'r') as f:
        notebook_content = json.loads(f.read())

    manifest = next(
        (notebook_content['cells'][0]['source']
         for index, cell in enumerate(notebook_content['cells'])
         if index == 0 and ''.join(cell['source']).replace('\n', '').startswith('manifest')), '')
    manifest = ''.join(manifest).replace('\n', '')
    manifest = config_to_dict(manifest, 'manifest') if manifest else {}
    if 'error' in manifest:
        message = {
            'error': 'Save notebook {0} failed'.format(notebook_path),
            'description': 'Parse manifest failed, Invalid format of manifest',
            'status': 400
        }
        logger.error(message)
        return message

    message = {
        'message': 'Save notebook {0} in progress'.format(notebook_path),
        'description': 'Manifest: {0}'.format(ujson.dumps(manifest))
    }

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

    if 'requirements' in manifest:
        requirements = requirements + '\n'.join(manifest['requirements'])

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
        startup_mapping = {
            'notebook_name': notebook_name,
        }
        with open(os.path.join(output_dir, 'startup.sh'), 'w') as f:
            f.write(JUPYTER_API_STARTUP.format_map(startup_mapping))

    manifest_yml={
        'application':[
            {'name': data['name'],
             'command': data['command'],
             'memory': data['memory'],
             'disk_quota': data['disk_quota'],
             'buildpack': data['buildpack'],
             'type': data['type'],
             # 'env': data['environment_json']
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
        config = ujson.loads(config)
    except ValueError:
        try:
            config = ast.literal_eval(config)

        except SyntaxError as e:
            message = {
                'error': 'Config parse error',
                'description': str(e),
                'status': 400
            }
            logger.error(message)
            return message

    return config
