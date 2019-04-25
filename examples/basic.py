from afs import AFSClient

# Initialize the AFSClient
afs_client = AFSClient(
    api_endpoint="Your AFS API endpoint",
    username="Your EI-PaaS SSO username",
    password="Your EI-PaaS SSO password",
)

# Or

afs_client = AFSClient(
    api_endpoint="Your AFS API endpoint", token="Your EI-PaaS SSO token"
)

# List all instances
instances = afs_client.instances()

# Get a instance by uuid
instance_id = "Your AFS instance_id"
instance = afs_client.instances.get(instance_id)

# Create a new model repository
model_repository_name = "Your model repository name"
model_repository = instance.model_repositories.create(name=model_repository_name)

# Upload model
model_name = "Your model name"
model = model_repository.models.create(name=model_name, model_path="Your model path")
