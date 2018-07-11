# AFS SDK

## 安裝
### pip install


version latest
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


## 支援python版本
python-3.X

## version 1.2.8 新增
Module
 
* join_table

## version 1.2.0 新增
Module

* config_handler: 提供開發者用於Online Flow IDE串接資料之SDK。使用範例[連結](examples/adder/adder_0509.md)。


## models usage
### 上傳training model
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


## Eamples
### upload training models function (On AFS developer)
```
from afs import models
with open('model.h5', 'w') as f:
    f.write('dummy model')
afs_models = models()
afs_models.upload_model('model.h5', accuracy=0.4, loss=0.3, tags=dict(machine='machine01'))
# 執行成功不回傳，執行失敗將raise原因
```


### upload training models function (Local developer)
```
from afs import models
with open('model.h5', 'w') as f:
    f.write('dummy model')
client = models(afs_url, instance_id, auth_code )
client.upload_model('model.h5', accuracy=0.4, loss=0.3, tags=dict(machine='machine01'))
# 執行成功不回傳，執行失敗將raise原因
```