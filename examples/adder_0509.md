

```python
manifest = {
    'memory': 256,
    'disk_quota': 256,
    'buildpack': 'python_buildpack',
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

## Input example in kernel gateway API
# REQUEST="""
# {
#     "headers": {
#         "Host": "140.92.24.91:9091",
#         "Connection": "keep-alive",
#         "Content-Length": "61",
#         "Origin": "chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop",
#         "Flow_id": "6805569a.b11218",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
#         "Content-Type": "application/json",
#         "Cache-Control": "no-cache",
#         "Host_url": "123",
#         "Node_id": "ada49faf.e05cf",
#         "Postman-Token": "17190eb2-0bff-f66a-b146-1e96bc8ce97a",
#         "Accept": "*/*",
#         "Accept-Encoding": "gzip, deflate",
#         "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
#     },
#     "body": {
#         "data": {
#             "value": {
#                 "0": 21
#             }
#         }
#      }
# }
# """

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


```python
# !pip uninstall -y afs
# !pip install https://github.com/benchuang11046/afs/archive/model-dev.zip

```
