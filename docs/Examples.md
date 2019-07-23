
# Examples

## models

### upload_model

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

# Upload the model to repository and the repository name is the same as file name, the the following is optional parameters:
#   1. (optional) accuracy is a evaluation of the model by the result of testing.
#   2. (optional) loss is a evaluation of the model by the result of testing.
#   3. (optional) extra_evaluation is for other evaluations for the model, you can put them to this parameter.
#   4. (optional) tags is the label for the model, like the time of data or the type of the algorithm.
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


###  download_model

**Code**
```
from afs import models

# Model object
afs_models = models()

# Download model from model repository, and get the last one model.
afs_models.download_model(save_path='dl_model.h5', model_repository_name='model.h5', last_one=True)

# Or get the specific model name in the model repository.
afs_models.download_model(save_path='dl_model.h5', model_repository_name='model.h5', model_name='2019-07-10 02:59:11.610828')

# List the directory
!ls
```

**Output**
```
dl_model.h5 
```



### upload_model (big model)

How to upload a big model (300MB-1GB) file on notebook. 

Both `encode_blob_accessKey` and `encode_blob_secretKey` can be gotten from encoded blob credential `accessKey` and `blob_secretKey` by `base64`. Developer can use `python` to encode or use web tool like [utilities-online](http://www.utilities-online.info/base64/#.XRG3H9MzbOQ).


**Code**

```
from afs import models

# Write a big file as 301 MB model file.
f = open('big_model.h5', "wb")
f.seek((301 * 1024 * 1024 + 1) - 1)
f.write(b"\0")
f.close()

# User-define evaluation result
extra_evaluation = {
    'AUC': 1.0
}

# User-define Tags 
tags = {'machine': 'machine01'}

# Model object
afs_models = models()
afs_models.set_blob_credential(
	blob_endpoint="http://x.x.x.x:x",
	encode_blob_accessKey="ENCODE_BLOB_ACCESSKEY", 
	encode_blob_secretKey="ENCODE_BLOB_SECRETKEY"
	)


# Upload the model to repository and the repository name is the same as file name.
# Accuracy and loss is necessary, but extra_evaluation and tags are optional.
afs_models.upload_model(
    model_path='big_model.h5', accuracy=0.4, loss=0.3, extra_evaluation=extra_evaluation, tags=tags, model_repository_name='model.h5')

```


**Output**
```
{
	'uuid': '433184a2-e930-465d-8b03-ecf0d649a7f9',
	'name': '2019-06-25 01:42:44.810366',
	'model_repository': 'bff9ea46-8856-4eef-b8dc-a4879a6ed9f9',
	'owner': 'dd9fcd3b-cfe7-47ec-9452-5157efcf1e50',
	'evaluation_result': {
		'accuracy': 0.4,
		'loss': 0.3,
		'AUC': 1.0
	},
	'parameters': {},
	'tags': {
		'machine': 'machine01'
	},
	'size': 315621377,
	'created_at': '2019-06-25T01:42:44.821000+00:00'
}
```


### [Advanced] Token download_model


**Code**
```
from afs import models

# AFS connect info. 
# Example format, CANNOT COPY AND PASTE.
# AFS API target endpoint
target_endpoint="https://api.afs.wise-paas.com"

# AFS service instance id
instance_id="123e4567-e89b-12d3-a456-426655440000"

# WISE-PaaS SSO token be gotten from SSO authentication
token="eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vdWFhLmFyZmEud2lzZS1wYWFzLmNvbS90b2tlbl9rZXlzIiwia2lkIjoia2V5LTEiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiJjZWExYTMwMGNjMmY0YzczYmMyNmY3Y2FiNTIwYjI4YSIsInN1YiI6IjhiNTJjODk0LTkyNmEtNDA4Mi1iNTdlLTc4ZDYwNjQ5MzI2OSIsInNjb3BlIjpbImNsb3VkX2NvbnRyb2xsZXIucmVhZCIsInBhc3N3b3JkLndyaXRlIiwiY2xvdWRfY29udHJvbGxlci53cml0ZSIsIm9wZW5pZCIsInVhYS51c2VyIl0sImNsaWVudF9pZCI6ImNmIiwiY2lkIjoiY2YiLCJhenAiOiJjZiIsImdyYW50X3R5cGUiOiJwYXNzd29yZCIsInVzZXJfaWQiOiI4YjUyYzg5NC05MjZhLTQwODItYjU3ZS03OGQ2MDY0OTMyNjkiLCJvcmlnaW4iOiJ1YWEiLCJ1c2VyX25hbWUiOiJCZW4yMDE5LkNodWFuZ0BhZHZhbnRlY2guY29tLnR3IiwiZW1haWwiOiJCZW4yMDE5LkNodWFuZ0BhZHZhbnRlY2guY29tLnR3IiwiYXV0aF90aW1lIjoxNTYyODM2ODA0LCJyZXZfc2lnIjoiNGU4NGIyOTQiLCJpYXQiOjE1NjM0NDQwOTksImV4cCI6MTU2MzQ0NDY5OSwiaXNzIjoiaHR0cHM6Ly91YWEuYXJmYS53aXNlLXBhYXMuY29tL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiYXVkIjpbImNsb3VkX2NvbnRyb2xsZXIiLCJwYXNzd29yZCIsImNmIiwidWFhIiwib3BlbmlkIl19.R1SHUv8CIIoEN1pL5aGjxTn3OMB1rgjumD0hFFFrqNVIwcctN4QvNH1kK6G6SZyrlXvjU_TXNDAbsAXiWLUkG7L60GZR2ZpJyPGNemZITjffuCKi0paQOrmAW5S0Nvn505G955DbuGDMGxQPOaorAcOkJYzFfAujSoZk3KMZmId9ACXr_Z96Fx5yhYnfXjT9aZDsASsx9I5UHYpunHRbzINJFx2PIxrYwCzfX2vFJqgeqeyeE1rjRsoS6GRj7eM3ud4YKQaC-MK0TFttkTeRtPwggUJV51QhDmH03EYQ5qVFqsixE_zPGKFQb4wnTkdWGUOyBjoYSTuzk_dUZNbHGG"

# Model object
my_models = models(
    target_endpoint=target_endpoint,
    instance_id=instance_id,
    token=token,
)

# Download model from model repository, and get the last one model.
afs_models.download_model(save_path='dl_model.h5', model_repository_name='model.h5', last_one=True)

# Or get the specific model name in the model repository.
afs_models.download_model(save_path='dl_model.h5', model_repository_name='model.h5', model_name='2019-07-10 02:59:11.610828')

# List the directory
!ls
```

**Output**
```
dl_model.h5 
```