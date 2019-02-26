$ eipaas-afs --help
Usage: eipaas-afs [OPTIONS] COMMAND [ARGS]...

Options:
  --version
  --ssl-verify / --skip-ssl-verify
                                  To verify SSL of API endpoint or not.
                                  Default is True.
  --help                          Show this message and exit.

Commands:
  create-model
  create-model-repo
  delete-model
  delete-model-repo
  instances
  login
  model-repos
  models
  target

$ eipaas-afs --version
2.1.2

$ eipaas-afs login
Api endpoint: YOUR_AFS_API_ENDPOINT
Username: YOUR_USERNAME
Password: 
Login to YOUR_AFS_API_ENDPOINT as user YOUR_USERNAME succeeded

$ eipaas-afs instances
784ce90a-c656-47a7-b4b1-755e62eaa676
81f894cd-d05b-4048-bbb8-bc20fb74ebf0
49cb2807-02fb-446b-a250-f06fd7531515

$ eipaas-afs target
Target to instance bab17642-e559-455b-a49b-832a84d4933c succeded

$eipaas-afs model-repos
model_repo-xxx
model_repo-yyy

$ eipaas-afs create-model-repo new_model_repo
Create model repository new_model_repo succeeded

$ eipaas-afs delete-model-repo new_model_repo
Delete model repository new_model_repo succeeded

$ eipaas-afs models new_model_repo
model-xxx
model-yyy

$ eipaas-afs create-model new_model_repo new_model YOUR_MODEL_PATH
Create model new_model succeeded

$ eipaas-afs delete-model new_model_repo new_model
Delete model new_model succeeded

$ eipaas-afs download-model new_model_repo new_model -p new_model.pkl
Download model new_model to path new_model.pkl succeeded
