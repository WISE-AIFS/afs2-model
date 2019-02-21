from afs import AFSClient

# Initialize the AFSClient
afs_client = AFSClient(
    api_endpoint='Your AFS API endpoint',
    username='Your EI-PaaS SSO username',
    password='Your EI-PaaS SSO password'
)

# Get your instance
instance_id = 'Your AFS instance_id'
instance = afs_client.instances.get(instance_id)

# Get your model repository
model_repo_id = 'Your model repository id'
model_repository = instance.model_repositories.get(model_repo_id)

# Write a file as model file.
model_path = 'model.h5'
with open(model_path, 'w') as f:
    f.write('dummy model')

# User defined evaluation result
evaluation_result = {
    'confusion_matrix_TP': 0.9,
    'confusion_matrix_FP': 0.8,
    'confusion_matrix_TN': 0.7,
    'confusion_matrix_FN': 0.6,
    'AUC': 1.0
}

# User defined tags
tags = {'machine': 'machine01'}

# Create new model
model_name = 'Your model name'
model = model_repository.models.create(
    name=model_name,
    model_path=model_path,
    evaluation_result=evaluation_result,
    tags=tags
)

# Get model info
print(model)
