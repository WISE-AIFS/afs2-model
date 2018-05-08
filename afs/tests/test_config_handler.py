
from afs import config_handler
import json

flow_json_file='add_node.json'
REQUEST="""
{
	"headers": {
		"node_id": "ada49faf.e05cf",
		"flow_id": "6805569a.b11218",
		"host_url": ""
	},
	"body": {
		"data": {
			"value": {
				"0": 21
			}
		}
	}
}
"""


cfg = config_handler()
cfg.set_param('b', type='integer', required=True, default=10)
cfg.set_column('a')
cfg.summary()

cfg.set_kernel_gateway(REQUEST, flow_json_file=flow_json_file)
b = cfg.get_param('b')
a = cfg.get_data()
result = a + b
ret = cfg.next_node(result, debug=True)
print(json.dumps(ret))