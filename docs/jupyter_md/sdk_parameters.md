

```python
manifest = {
    'memory': 256,
    'disk_quota': 256,
    'buildpack': 'python_buildpack',
    "requirements":[
        "pandas",
        "afs"
    ],
    'type': 'API'
}
```


```python
from afs import config_handler
from pandas import DataFrame
import json

# Setting API parameters
cfg = config_handler()
cfg.set_param('mystring', type='string', required=True, default='mystring')
cfg.set_param('myinterger', type='integer', required=True, default=111)
cfg.set_param('myfloat', type='float', required=True, default=2.345)
cfg.set_param('mylist', type='list', required=True, default=[1,2,3])
cfg.summary()
```

    {"features": false, "param": [{"name": "mystring", "type": "string", "required": true, "default": "mystring"}, {"name": "myinterger", "type": "integer", "required": true, "default": 111}, {"name": "myfloat", "type": "float", "required": true, "default": 2.345}, {"name": "mylist", "type": "list", "required": true, "default": [1, 2, 3]}], "column": []}



```python
# POST /

# Set flow architecture, REQUEST is the request including body and headers from client
cfg.set_kernel_gateway(REQUEST)

# Get the parameter from node-red setting
mystring = cfg.get_param('mystring')
myinterger = cfg.get_param('myinterger')
myfloat = cfg.get_param('myfloat')
mylist = cfg.get_param('mylist')

# The printing is the API response.
print('mysting: {0}'.format(mystring))
print('myinterger: {0}'.format(myinterger))
print('myfloat: {0}'.format(myfloat))
print('mylist: {0}'.format(mylist))

```
