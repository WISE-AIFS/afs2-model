

```python
manifest = {
    'memory': 512,
    'disk_quota': 512,
    'buildpack': 'python_buildpack',
    'requirements': [
        'git+https://github.com/benchuang11046/afs.git'
    ],
    'type': 'API'
}
```


```python
input_type = {
    "param": [
        {
            "name": "frequency",
            "type": "text",
            "default": 30
        },
        {
            "name": "password",
            "type": "password"
        }
    ],
    "column": ["AE_TEMPERATURE", "timestamp"]
}
```


```python
from afs import flow
```


```python
def analytic_func(data, config):
    freq = config['frequency']
    password = config['password']
    
    result = train(dataframe, freq)
    access_database(password)
    
    return result
```


```python
# POST /
afs_flow = flow(REQUEST, input_type) 
    # REQUEST: JSON from request, input_type: 2nd Cell content
resp_body = analytic_func(afs_flow.dataframe, afs_flow.config) 
    # dataframe: Dataframe, afs_flow.param: Dict, afs_flow.resp_body: Dict
afs_flow.respond(resp_body)
    # return resp_body
```


```python
REQUEST['body']
REQUEST['headers']

```
