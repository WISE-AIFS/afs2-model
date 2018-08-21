
# Examples

## models

### upload_models
```
from afs import models

with open('model.h5', 'w') as f:
    f.write('dummy model')

eval_dict = {
    'confusion_matrix': {
        'TP': 0.9,
        'FP': 0.8,
        'TN': 0.7,
        'FN': 0.6
    },
    'AUC': 1.0
}

tags = {'machine': 'machine01'}

afs_models = models()
afs_models.upload_model(
    'model.h5', accuracy=0.4, loss=0.3, extra_evaluation=eval_dict, tags=tags)
```


## config_handler

### Features
How to write a AFS API to get features, including target, select_features, numerical. [[Example](jupyter_md/sdk_featrues.md)]

### Parameter (Type list)
How to write a AFS API to get parameters with the list type.  [[Example](jupyter_md/sdk_para_list.md)]

