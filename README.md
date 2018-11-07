# AFS SDK

[![Documentation Status](https://readthedocs.org/projects/afs-docs/badge/?version=latest)](https://afs-docs.readthedocs.io/en/latest/?badge=latest)


## Documents
Reference documents [Readthedocs](http://afs-docs.readthedocs.io/en/latest/sdk/)


## Installation

Support python version 3.5 or later


### pip install on AFS online code IDE
 
### On public cloud (RELEASE)
```
pip install https://github.com/benchuang11046/afs/releases/download/1.2.27/afs-1.2.27-py3-none-any.whl
```


#### On private cloud

[Install Documents](https://afs-docs.readthedocs.io/en/latest/sdk/docs/InstallDependencies.html)

### (For SDK developer) pip install the latest version

*The latest develop version*
```
$ pip install git+https://github.com/benchuang11046/afs.git
```

### (For SDK developer) From sources

1. Clone the repository to local.

2. To build the library run:
```
$ python setup.py install
```

### (For SDK developer) Build from source

1. Clone the repository to local.

2. To build the wheel package:
```
$ python setup.py bdist_wheel
```

3. .whl will be in dist/ 