# AFS SDK

## 安裝

pip install

```
$ pip install git+http://140.92.25.64:8888/estherxchl/afs_project.git
```

From sources

To build the library run :
```
$ pip install requirements
$ python setup.py install
```

## 用法

上傳model
```
def upload_model(self, model_name, accuracy, loss, tags={}, extra_evaluation={}):
```


## 範例

```
from afs.client import afs
client = afs()
client.models.upload_model('model.h5', accuracy=0.4, loss=0.3, tags=dict(machine='machine01'))
# 回傳True代表成功上傳model
```

