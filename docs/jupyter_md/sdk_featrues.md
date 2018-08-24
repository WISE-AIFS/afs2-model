

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

# Setting API parameters and column name
cfg = config_handler()
cfg.set_features(True)
cfg.summary()
```

    {"features": true, "param": [], "column": []}



```python
# POST /

# Set flow architecture, REQUEST is the request including body and headers from client
cfg.set_kernel_gateway(REQUEST)

# Get features.(target, select_features, numerical)
ft = cfg.get_features_target()
fs = cfg.get_features_selected()
fn = cfg.get_features_numerical()

# The printing is the API response.
print('target:{0}'.format(ft))
print('select_features:{0}'.format(fs))
print('numerical:{0}'.format(fn))

```
