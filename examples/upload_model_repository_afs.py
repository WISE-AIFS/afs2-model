import os
from afs2_model import AFSClient

api_endpoint = os.getenv('afs_url')
instance_id = os.getenv('instance_id')
username = "username"
password = "password"

# Initialize the AFSClient
afs_client = AFSClient(
    api_endpoint=api_endpoint,
    username=username,
    password=password,
)

# Get your instance
instance = afs_client.instances.get(instance_id)

# Get your model repository
model_repo_name = "TestModelRepo"
find_repo = instance.model_repositories(uuid=None, q='name:{0}'.format(model_repo_name))
model_repo_id = find_repo.pop()['uuid']
model_repository = instance.model_repositories.get(model_repo_id)

# Write a file as model file.
model_path = "model.h5"
with open(model_path, "w") as f:
    f.write("dummy model")

# User defined evaluation result
evaluation_result = {
    "confusion_matrix_TP": 0.9,
    "confusion_matrix_FP": 0.8,
    "confusion_matrix_TN": 0.7,
    "confusion_matrix_FN": 0.6,
    "AUC": 1.0,
}

# User defined tags
tags = {"machine": "machine01"}

# Create new model
model_name = "Your model name"
model = model_repository.models.create(
    name=model_name,
    model_path=model_path,
    evaluation_result=evaluation_result,
    tags=tags,
)

# Get model info
print(model)