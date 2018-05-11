

```python
manifest = {
    'memory': 256,
    'disk_quota': 256,
    'buildpack': 'python_buildpack',
    "requirements":[
        "pandas",
        "https://github.com/benchuang11046/afs/archive/QA.zip"
    ],
    'type': 'API'
}
```


```python
from afs import config_handler
from pandas import DataFrame
import json

# Setting API parameters and column name
cfg = config_handler()
cfg.set_param('b', type='integer', required=True, default=10)
cfg.set_column('a')
cfg.summary()
```


```python
# POST /

# Set flow architecture, REQUEST is the request including body and headers from client
cfg.set_kernel_gateway(REQUEST)

# Get the parameter from node-red setting
b = cfg.get_param('b')

# Get the data from request, and transform to DataFrame Type
a = cfg.get_data()
result = a + b

# Send the result to next node, and result is  DataFrame Type
ret = cfg.next_node(result, debug=True)

# The printing is the API response.
print(json.dumps(ret))
```

