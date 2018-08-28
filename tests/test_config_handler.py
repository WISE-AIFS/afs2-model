import json

def test_config_handler_para_feature_data(config_handler_resource, capsys):
    config_handler_resource.set_param('myinteger', type='integer', required=True, default=2)
    config_handler_resource.set_param('myfloat', type='float', required=True, default=2.345)
    config_handler_resource.set_param('mystring', type='string', required=True, default='ms')
    config_handler_resource.set_param('mylist', type='list', required=True, default=['a','b'])
    config_handler_resource.set_features(True)
    config_handler_resource.set_column('mycolumn')
    config_handler_resource.summary()

    out, err = capsys.readouterr()
    assert json.loads(out) == json.loads("""
{"features": true, "param": [{"name": "myinteger", "type": "integer", "required": true, "default": 2}, {"name": "myfloat", "type": "float", "required": true, "default": 2.345}, {"name": "mystring", "type": "string", "required": true, "default": "ms"}, {"name": "mylist", "type": "list", "required": true, "default": ["a", "b"]}], "column": ["mycolumn"]}
""")
    REQUEST = """
    {"headers": {"Flow_id": "2c3e36f5.79745a",  "Node_id": "7d3b635a.f0a75c"}, "body": {"data": {"mc": {"0": 21}}}}
    """
    flow_json = """
{"id": "2c3e36f5.79745a", "label": "test parser", "nodes": [{"id": "1603f0e2.15482f", "type": "sso_setting", "z": "2c3e36f5.79745a", "name": "sso wise-paas", "sso_user": "wisepaas.qa@devops.com.cn", "sso_password": "P@ssw0rd/", "x": 150, "y": 80, "wires": []}, {"id": "5da078ac.7ab548", "type": "firehose_influxdb_query", "z": "2c3e36f5.79745a", "name": "arfa titanic", "url": "", "_node_type": "firehose", "sso_token": "", "service_name": "influxdb_demo", "service_key": "influxdb_demo", "service_credentials": {}, "feature_names": ["time", "Age", "Embarked", "Fare", "Name", "PassengerId", "Pclass", "Sex", "SibSp", "Survived"], "query": "select * from titanic_data", "x": 160, "y": 140, "wires": [[]]}, {"id": "7d3b635a.f0a75c", "type": "test_node", "z": "2c3e36f5.79745a", "name": "test_sdk", "myinteger": 2, "myfloat": 2.123, "mystring": "abcde", "mylist": ["abc", "def", "ghi"], "mycolumn": "mc", "url": "", "target": "tar_1", "select_feature": ["sel_1", "sel_2", "sel_3", "sel_4"], "numerical": ["num_1", "num_2"], "x": 340, "y": 120, "wires": [[]]}]}
    """

    config_handler_resource.set_kernel_gateway(REQUEST, flow_json_file=flow_json)

    mi = config_handler_resource.get_param('myinteger')
    mf = config_handler_resource.get_param('myfloat')
    ms = config_handler_resource.get_param('mystring')
    ml = config_handler_resource.get_param('mylist')
    data = config_handler_resource.get_data()
    assert isinstance(mi, int)
    assert mi == 2
    assert isinstance(mf, float)
    assert mf == 2.123
    assert isinstance(ms, str)
    assert ms == "abcde"
    assert isinstance(ml, list)
    assert ml == ["abc", "def", "ghi"]
    assert data['mycolumn'][0] == 21

    ft = config_handler_resource.get_features_target()
    assert isinstance(ft, str)

    fs = config_handler_resource.get_features_selected()
    assert isinstance(list(ft), list)

    fn = config_handler_resource.get_features_numerical()
    assert isinstance(list(fn), list)

    # ret = config_handler_resource.next_node(result, debug=False)
    # print(json.dumps(ret))
    #
    # assert ret[0] == '0'
    # assert ret[1] == ''

