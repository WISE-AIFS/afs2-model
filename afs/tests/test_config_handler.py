
from afs import config_handler
import json

cfg = config_handler()
cfg.set_param('b', type='integer', required=True, default=10)
cfg.set_column('value')
cfg.summary()

with open('add_node.json') as f:
    flow_json = f.read()
flow_json = json.loads(flow_json)
flow_json = json.dumps(flow_json)
print(flow_json)

req_body = {'data': {'value': {'0': 21}}, 'node_id': 'ada49faf.e05cf'}
req_body = json.dumps(req_body)

cfg.set_flow(flow_json, req_body)
b = cfg.get_param('b')
a = cfg.get_data(req_body)
result = a + b
cfg.next_node(result)