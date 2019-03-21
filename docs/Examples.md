
# Examples

## models

### upload_models

How to upload a model file on notebook. 

**Code**

```
from afs import models

# Write a file as model file.
with open('model.h5', 'w') as f:
    f.write('dummy model')

# User-define evaluation result
extra_evaluation = {
    'confusion_matrix_TP': 0.9,
    'confusion_matrix_FP': 0.8,
    'confusion_matrix_TN': 0.7,
    'confusion_matrix_FN': 0.6,
    'AUC': 1.0
}

# User-define Tags 
tags = {'machine': 'machine01'}

# Model object
afs_models = models()

# Upload the model to repository and the repository name is the same as file name.
# Accuracy and loss is necessary, but extra_evaluation and tags are optional.
afs_models.upload_model(
    model_path='model.h5', accuracy=0.4, loss=0.3, extra_evaluation=extra_evaluation, tags=tags, model_repository_name='model.h5')

# Get the latest model info 
model_info = afs_models.get_latest_model_info(model_repository_name='model.h5')

# See the model info
print(model_info)
```

**results**
```
{
	'evaluation_result': {
		'accuracy': 0.4,
		'loss': 0.3,
		'confusion_matrix': {
			'TP': 0.9,
			'FP': 0.8,
			'TN': 0.7,
			'FN': 0.6
		},
		'AUC': 1.0
	},
	'tags': {
		'machine': 'machine01'
	},
	'created_at': '2018-12-06 08:41:39'
}
```


### get_latest_model_info

**Code**
```
from afs import models
afs_models = models()
afs_models.get_latest_model_info(model_repository_name='model.h5')
```

**Output**
```
{
	'evaluation_result': {
		'accuracy': 0.123,
		'loss': 0.123
	},
	'tags': {},
	'created_at': '2018-09-11 10:15:54'
}
```
