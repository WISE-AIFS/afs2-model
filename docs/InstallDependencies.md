

# Install AFS-SDK without external network
If you want install AFS-SDK without external network, you should install dependency step by step. The following is afs-sdk dependency tree:

## How to check out the dependency tree command 
```
! pip install pipdeptree
! pipdeptree -fl
```

![afs_pipdeptree](_static/images/pipdeptree.PNG)

## How to install module on private cloud

[Install module with Vendor in private cloud](https://afs-docs.readthedocs.io/en/latest/portal/workspace.html#install-module-with-vendor-in-private-cloud)


## AFS-SDK dependency tree
Install dependency module first.

### afs==1.2.19
```
afs
  click
  influxdb
    python-dateuti
      six
    pytz
    requests
      certifi
      chardet
      idna
      urllib3
    six
  pandas
    numpy
    python-dateutil
      six
    pytz
  PyYAML
  requests
    certifi
    chardet
    idna
    urllib3
  urllib3
```

There is a script for installing dependency quickly on AFS online code IDE. And replace the instance_id and workspace_id.


**Script**
```
import os

# check pkg config, instance id, workspace_id
pkg = ['urllib3-1.23-py2.py3-none-any.whl', 'six-1.11.0-py2.py3-none-any.whl', 'python_dateutil-2.7.3-py2.py3-none-any.whl', 'chardet-3.0.4-py2.py3-none-any.whl', 'certifi-2018.4.16-py2.py3-none-any.whl', 'idna-2.7-py2.py3-none-any.whl', 'click-6.7-py2.py3-none-any.whl', 'requests-2.19.1-py2.py3-none-any.whl', 'influxdb-5.2.0-py2.py3-none-any.whl', 'afs-1.2.19.dev-py3-none-any.whl']
instance_id = '****' 
workspace_id = '****'

install_cmd = '$afs_url/v1/{0}/workspaces/{1}/vendor/'.format(instance_id, workspace_id)
auth_cmd = '?auth_code=$auth_code'

# loop install
for i in pkg:
    cmd = '{0}{1}{2}'.format(install_cmd, i, auth_cmd)
    os.environ['cmd'] = cmd
    !pip install $cmd
```


## (For developer) Build AFS-SDK whl  
To build the wheel module:
```
$ python setup.py bdist_wheel
```

AFS-SDK whl file will be in dist/ directory.
