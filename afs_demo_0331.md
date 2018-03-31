

```python
!pip install git+https://github.com/benchuang11046/afs.git
```

    Collecting git+https://github.com/benchuang11046/afs.git
      Cloning https://github.com/benchuang11046/afs.git to /home/vcap/tmp/pip-xwj1vri8-build
    Requirement already satisfied: requests in /home/vcap/app/.cloudfoundry/0/python/lib/python3.5/site-packages (from afs==1.0.0)
    Requirement already satisfied: certifi>=2017.4.17 in /home/vcap/app/.cloudfoundry/0/python/lib/python3.5/site-packages (from requests->afs==1.0.0)
    Requirement already satisfied: idna<2.7,>=2.5 in /home/vcap/app/.cloudfoundry/0/python/lib/python3.5/site-packages (from requests->afs==1.0.0)
    Requirement already satisfied: urllib3<1.23,>=1.21.1 in /home/vcap/app/.cloudfoundry/0/python/lib/python3.5/site-packages (from requests->afs==1.0.0)
    Requirement already satisfied: chardet<3.1.0,>=3.0.2 in /home/vcap/app/.cloudfoundry/0/python/lib/python3.5/site-packages (from requests->afs==1.0.0)
    Installing collected packages: afs
      Running setup.py install for afs ... [?25ldone
    [?25hSuccessfully installed afs-1.0.0
    [33mYou are using pip version 9.0.1, however version 9.0.3 is available.
    You should consider upgrading via the 'pip install --upgrade pip' command.[0m



```python
from afs.client import afs

with open('model.h5', 'w') as f:
    f.write('dummy model')
client = afs()
client.models.upload_model('model.h5', accuracy=0.4, loss=0.3, tags=dict(machine='machine01'))
```
