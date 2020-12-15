
# Examples

## models

### upload_model

How to upload a model file(<1GB) on notebook.  

**Code**

```
from afs import models

# Write a file as model file.
with open('model.h5', 'w') as f:
    f.write('dummy model')

# User-define evaluation result. Type:dict
extra_evaluation = {
    'confusion_matrix_TP': 0.9,
    'confusion_matrix_FP': 0.8,
    'confusion_matrix_TN': 0.7,
    'confusion_matrix_FN': 0.6,
    'AUC': 1.0
}

# User-define Tags. Type:dict
tags = {'machine': 'machine01'}

# User-define Feature Importance Type:list(dict)
feature_importance = [
	{'feature': 'petal_length', 'importance': 0.9473576807512394}, 
	{'feature': 'petal_width',  'importance': 0.038191635936882906}, 
	{'feature': 'sepal_length', 'importance': 0.011053241240641932}, 
	{'feature': 'sepal_width',  'importance': 0.0033974420712357825}
]

coefficient = [
	{'feature': 'B-0070-0068-1-FN66F_strength', 'coefficient': -4.730741400252476}, 
	{'feature': 'B-0070-0068-1-FN66F_vendor', 'coefficient': -0.9335123601234512}, 
	{'feature': 'B-0070-0068-1-FN66F_tensile','coefficient': 0.16411707246054036}, 
	{'feature': 'B-0070-0068-1-FN66F_lot','coefficient': -0.08745686004816221}, 
	{'feature': 'Machine','coefficient': 0.015048547152059243}, 
	{'feature': 'Lot','coefficient': -0.010971975766858174}, 
	{'feature': 'RPM','coefficient': 0.0003730247816832932}, 
	{'feature': 'record_purpose','coefficient': 0.0}
]

# User-define RSA Public key Type:string
encrypt_key = """-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAJrX4NIpPBdsOoFDo6oTUiRVM2CCYF/wdCy/KZ54mHyPRRFwtxcuRYt5omODY8uh
zTWjkb0jv0JphsHJmjeYkggHUxTrWeJ2gPfReTKPfmIGP0BQhHtwb92gxPYiJVHjSVgLLOe2
75iRyb7a5N20eiw5bEB4IFsuy+QXbDvUUsNPAgMBAAE=
-----END RSA PUBLIC KEY-----
"""

# Model object
afs_models = models()

# Upload the model to repository and the repository name is the same as file name, the the following is optional parameters:
#   1. (optional) accuracy is a evaluation of the model by the result of testing.
#   2. (optional) loss is a evaluation of the model by the result of testing.
#   3. (optional) extra_evaluation is for other evaluations for the model, you can put them to this parameter.
#   4. (optional) tags is the label for the model, like the time of data or the type of the algorithm.
#   5. (optional) feature_importance is the record how the features important in the model.
#	6. (optional) coefficient indicates the direction of the relationship between a predictor variable and the response variable.
#   7. (optional) If there is a encrypt_key, use the encrypt_key to encrypt the model
afs_models.upload_model(
    model_path='model.h5',
	model_repository_name='model.h5',
	accuracy=0.4,
	loss=0.3, 
	extra_evaluation=extra_evaluation, 
	tags=tags,
	feature_importance=feature_importance,
	coefficient=coefficient,
	encrypt_key=encrypt_key
)

# Get the latest model info 
model_info = afs_models.get_latest_model_info(model_repository_name='model.h5')

# See the model info
print(model_info)
```

**results**
```
{
	'uuid': '3369315c-d652-4c4d-b481-405be2ad5b33',
	'name': '3369315c-d652-4c4d-b481-405be2ad5b33',
	'model_repository': 'ef388859-64fb-4718-b90f-34defc8a3aae',
	'owner': '12345338-62b6-11ea-b1de-d20dfb084846',
	'evaluation_result': {
		'accuracy': 0.4,
		'loss': 0.3,
		'confusion_matrix_TP': 0.9,
		'confusion_matrix_FP': 0.8,
		'confusion_matrix_TN': 0.7,
		'confusion_matrix_FN': 0.6,
		'AUC': 1.0
	},
	'tags': {
		'machine': 'machine01',
		'is_encrypted': True
	},
	'feature_importance': [{
		'feature': 'petal_length',
		'importance': 0.9473576808
	}, {
		'feature': 'petal_width',
		'importance': 0.0381916359
	}, {
		'feature': 'sepal_length',
		'importance': 0.0110532412
	}, {
		'feature': 'sepal_width',
		'importance': 0.0033974421
	}],
	'coefficient': [
		{'feature': 'B-0070-0068-1-FN66F_strength', 'coefficient': -4.730741400252476}, 
		{'feature': 'B-0070-0068-1-FN66F_vendor', 'coefficient': -0.9335123601234512}, 
		{'feature': 'B-0070-0068-1-FN66F_tensile','coefficient': 0.16411707246054036}, 
		{'feature': 'B-0070-0068-1-FN66F_lot','coefficient': -0.08745686004816221}, 
		{'feature': 'Machine','coefficient': 0.015048547152059243}, 
		{'feature': 'Lot','coefficient': -0.010971975766858174}, 
		{'feature': 'RPM','coefficient': 0.0003730247816832932}, 
		{'feature': 'record_purpose','coefficient': 0.0}
	],
	'size': 11,
	'created_at': '2020-04-06T10:23:56.228000+00:00'
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
afs_models.download_model(
	save_path='dl_model.h5', 
	model_repository_name='model.h5', 
	last_one=True)

# Or get the specific model name in the model repository.
afs_models.download_model(
	save_path='dl_model.h5', 
	model_repository_name='model.h5', 
	model_name='2019-07-10 02:59:11.610828')

# List the directory
!ls
```

**Output**
```
dl_model.h5 
```




###  decrypt_model

**Code**
```
from afs import models

decrypt_key = """-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQCCCmzSJsR2kb5Tol7RyNM19XIbXsYYjzNSA0maJ3lPDNnJE0Kb6bP2Au+Y
QOT6y9Mse/hqKkeXjpMaOBbx+5fGM5ivEJiqepRBdD3mbkJMhvnrNTR4hzYpUgD69d+LzZkp
Q4GBHR93LRYvdUaBrSDXH0G6BLFe3AGF44LoWEa5fQIDAQABAoGBAICWFmzncLVeADlrAR+n
2VIt1htCZ9e5IiIiphEMn2OPbXrq1J6fRRgqZwjCgqmMCtCd9VHlZM10afkvJWE6SySBHR2T
qsMTuvJfGAEIRKo19p6BSqxpSRitP/Ow3liaND0i8MTJ5ixaiOhmRUX2jlWM1XfhuUjF6YGV
ProlojMBAkEA0s6eyxTUjazAEVCQ9BeCorwF/FM9Nf+4ZShOlLJZ+eRwFa5Epeziu/ecVbzQ
jzDI1KWlj+Gxl35zl03ooA5JrQJBAJ3rPG8CJFafxi2WcORIhGr2R/tcJRGjJcutMyGpi+zH
k7+eNRt9ZBowwCkjeJh+MJmKwjZ0NToS8jGox2LHyRECQFQ20L7mSmdynKQOIGoyvjBOlsGP
a0OYLczThljmywUGWjR/EtOKR6W5rE2gCV06qvAwYGyTSAPyMzE9oXHXY10CQQAO5g2aj4Is
JgDFdkcKUokjqj6aSVQ5+MFtGNcVGvDXkvCuiFeMU2UpT2Yhu3X6NRWSttOh3Y7T/suYwcql
2CFxAkEAu+c3M1YSCpUZLdne9EW18/+4wWYNuFSOuGVK0FUyjjNhWzfDFARYNFgR+5mUMaJ0
4wNCyD5hvUVkBOZINHWtiw==
-----END RSA PRIVATE KEY-----
"""

# Model object
afs_models = models()

# Download model from model repository.
afs_models.download_model(
	save_path='dl_model.h5', 
	model_repository_name='model.h5', 
	last_one=True)

# Open the model and decrypt.
with open('dl_model.h5', 'rb') as f:
	data = f.read()
	model = afs_models.decrypt_model(data, decrypt_key
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
token="bearer eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vdWFhLmFyZmEud2lzZS1wYWFzLmNvbS90b2tlbl9rZXlzIiwia2lkIjoia2V5LTEiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiJjZWExYTMwMGNjMmY0YzczYmMyNmY3Y2FiNTIwYjI4YSIsInN1YiI6IjhiNTJjODk0LTkyNmEtNDA4Mi1iNTdlLTc4ZDYwNjQ5MzI2OSIsInNjb3BlIjpbImNsb3VkX2NvbnRyb2xsZXIucmVhZCIsInBhc3N3b3JkLndyaXRlIiwiY2xvdWRfY29udHJvbGxlci53cml0ZSIsIm9wZW5pZCIsInVhYS51c2VyIl0sImNsaWVudF9pZCI6ImNmIiwiY2lkIjoiY2YiLCJhenAiOiJjZiIsImdyYW50X3R5cGUiOiJwYXNzd29yZCIsInVzZXJfaWQiOiI4YjUyYzg5NC05MjZhLTQwODItYjU3ZS03OGQ2MDY0OTMyNjkiLCJvcmlnaW4iOiJ1YWEiLCJ1c2VyX25hbWUiOiJCZW4yMDE5LkNodWFuZ0BhZHZhbnRlY2guY29tLnR3IiwiZW1haWwiOiJCZW4yMDE5LkNodWFuZ0BhZHZhbnRlY2guY29tLnR3IiwiYXV0aF90aW1lIjoxNTYyODM2ODA0LCJyZXZfc2lnIjoiNGU4NGIyOTQiLCJpYXQiOjE1NjM0NDQwOTksImV4cCI6MTU2MzQ0NDY5OSwiaXNzIjoiaHR0cHM6Ly91YWEuYXJmYS53aXNlLXBhYXMuY29tL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiYXVkIjpbImNsb3VkX2NvbnRyb2xsZXIiLCJwYXNzd29yZCIsImNmIiwidWFhIiwib3BlbmlkIl19.R1SHUv8CIIoEN1pL5aGjxTn3OMB1rgjumD0hFFFrqNVIwcctN4QvNH1kK6G6SZyrlXvjU_TXNDAbsAXiWLUkG7L60GZR2ZpJyPGNemZITjffuCKi0paQOrmAW5S0Nvn505G955DbuGDMGxQPOaorAcOkJYzFfAujSoZk3KMZmId9ACXr_Z96Fx5yhYnfXjT9aZDsASsx9I5UHYpunHRbzINJFx2PIxrYwCzfX2vFJqgeqeyeE1rjRsoS6GRj7eM3ud4YKQaC-MK0TFttkTeRtPwggUJV51QhDmH03EYQ5qVFqsixE_zPGKFQb4wnTkdWGUOyBjoYSTuzk_dUZNbHGG"

# Model object
my_models = models(
    target_endpoint=target_endpoint,
    instance_id=instance_id,
    token=token,
)

# Download model from model repository, and get the last one model.
my_models.download_model(save_path='dl_model.h5', model_repository_name='model.h5', last_one=True)

# Or get the specific model name in the model repository.
my_models.download_model(save_path='dl_model.h5', model_repository_name='model.h5', model_name='2019-07-10 02:59:11.610828')

# List the directory
!ls
```

**Output**
```
dl_model.h5 
```