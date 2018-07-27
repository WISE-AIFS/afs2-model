# AFS SDK

[![Documentation Status](https://readthedocs.org/projects/afs-docs/badge/?version=latest)](https://afs-docs.readthedocs.io/en/latest/?badge=latest)


## Documents
Reference documents [Readthedocs](http://afs-docs.readthedocs.io/en/latest/sdk/)


## Installation

Support python version 3.5 later

### pip install


Version latest
```
$ pip install https://github.com/benchuang11046/afs.git
```

### From sources


To build the library run:
```
$ python setup.py install
```

To build the wheel package:
```
$ python setup.py bdist_wheel
```

## Version 1.2.8 
Module
 
* join_table

## Version 1.2.0
Module

* config_handler: Provide to developer SDK in Online FLow IDE. Example [link](examples/adder/adder_0509.md)

## models usage
### upload training model
```
def upload_model(model_name, accuracy, loss, tags={}, extra_evaluation={}):
        """
        Upload model_name to model repository.If model_name is not exists in the repository, this function will create one.
         :rtype: None
         :param model_name:  (required) string, model path or name
         :param accuracy: (required) float, model accuracy value
         :param loss: (required) float, model loss value
         :param tags: (optional) dict, tag from model
         :param extra_evaluation: (optional) dict, other evaluation from model
         """
```


## Examples
### upload training models function (On AFS developer)
```
from afs import models
with open('model.h5', 'w') as f:
    f.write('dummy model')
afs_models = models()
afs_models.upload_model('model.h5', accuracy=0.4, loss=0.3, tags=dict(machine='machine01'))
# success, or raise the reason
```


### upload training models function (Local developer)
```
from afs import models
with open('model.h5', 'w') as f:
    f.write('dummy model')
client = models(afs_url, instance_id, auth_code )
client.upload_model('model.h5', accuracy=0.4, loss=0.3, tags=dict(machine='machine01'))
#  success, or raise the reason
```