# AFS SDK

## 安裝

pip install

```
$ pip install git+https://github.com/benchuang11046/afs.git
```

From sources

To build the library run :
```
$ python setup.py install
```

## 用法

上傳model
```
def upload_model(model_name, accuracy, loss, tags={}, extra_evaluation={}):
        """
         :rtype: None
         :param model_name: (required) string, model path or name
         :param accuracy: (required) float, model accuracy value
         :param loss: (required) float, model loss value
         :param tags: (optional) dict, tag from model
         :param extra_evaluation: (optional) dict, other evaluation from model
         """
```


## 範例


### models function
```
from afs.client import afs
with open('model.h5', 'w') as f:
    f.write('dummy model')
client = afs()
client.models.upload_model('model.h5', accuracy=0.4, loss=0.3, tags=dict(machine='machine01'))
# 執行成功不回傳，執行失敗將raise原因
```

