
from afs import config_handler
import json

flow_json_file='add_node.json'
REQUEST="""
{
	"headers": {
		"Host": "140.92.24.91:9091",
		"Connection": "keep-alive",
		"Content-Length": "61",
		"Origin": "chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop",
		"Flow_id": "6805569a.b11218",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
		"Content-Type": "application/json",
		"Cache-Control": "no-cache",
		"Host_url": "123",
		"Node_id": "ada49faf.e05cf",
		"Postman-Token": "17190eb2-0bff-f66a-b146-1e96bc8ce97a",
		"Accept": "*/*",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
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