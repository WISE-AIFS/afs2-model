

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
cfg.set_param('feature_names', type='list', required=True, default=[1,2,3])
cfg.summary()
```

    {"features": false, "param": [{"name": "feature_names", "type": "list", "required": true, "default": [1, 2, 3]}], "column": []}



```python
# POST /

# Set flow architecture, REQUEST is the request including body and headers from client
cfg.set_kernel_gateway(REQUEST)

# Get the parameter from node-red setting
feature_names = cfg.get_param('feature_names')

# Send the result to next node, and result is DataFrame Type
ret = cfg.next_node(result, debug=False)

# The printing is the API response.
print(feature_names)
print(json.dumps(ret))
```
