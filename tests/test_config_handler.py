import json

def test_config_handler_adder_list_feature(config_handler_resource, capsys):
    config_handler_resource.set_param('feature_names', type='list', required=True, default=[1,2,3])
    config_handler_resource.set_param('b', type='integer', required=True, default=2)
    config_handler_resource.set_features(True)
    config_handler_resource.set_column('a')
    config_handler_resource.summary()

    out, err = capsys.readouterr()
    assert json.loads(out) == json.loads("""
    {"features": true, "param": [{"name": "feature_names", "type": "list", "required": true, "default": [1, 2, 3]}, {"name": "b", "type": "integer", "required": true, "default": 2}], "column": ["a"]}
""")

    REQUEST = """
    {"headers": {"Flow_id": "2c3e36f5.79745a",  "Node_id": "7d3b635a.f0a75c"}, "body": {"data": {"value": {"0": 21}}}}
    """
    flow_json = """
    {"id": "2c3e36f5.79745a", "label": "test parser", "nodes": [{"id": "1603f0e2.15482f", "type": "sso_setting", "z": "2c3e36f5.79745a", "name": "sso wise-paas", "sso_user": "wisepaas.qa@devops.com.cn", "sso_password": "P@ssw0rd/", "x": 150, "y": 80, "wires": []}, {"id": "5da078ac.7ab548", "type": "firehose_influxdb_query", "z": "2c3e36f5.79745a", "name": "arfa titanic", "url": "", "_node_type": "firehose", "sso_token": "", "service_name": "influxdb_demo", "service_key": "influxdb_demo", "service_credentials": {}, "feature_names": ["time", "Age", "Embarked", "Fare", "Name", "PassengerId", "Pclass", "Sex", "SibSp", "Survived"], "query": "select * from titanic_data", "x": 160, "y": 140, "wires": [[]]}, {"id": "7d3b635a.f0a75c", "type": "test_node", "z": "2c3e36f5.79745a", "name": "test_sdk", "b": 2, "url": "", "feature_names": ["time", "Age", "Embarked", "Fare", "Name", "PassengerId", "Pclass", "Sex", "SibSp", "Survived"], "target": ["tar_1", "tar_2", "tar_3"], "select_feature": ["sel_1", "sel_2", "sel_3", "sel_4"], "numerical": ["num_1", "num_2"], "x": 340, "y": 120, "wires": [[]]}]}
    """

    config_handler_resource.set_kernel_gateway(REQUEST, flow_json_file=flow_json)
    b = config_handler_resource.get_param('b')
    a = config_handler_resource.get_data()
    result = a + b
    assert result['value'][0] == 23

    feature_names = config_handler_resource.get_param('feature_names')
    assert len(feature_names) == 10

    ft = config_handler_resource.get_features_target()
    assert len(ft) == 3

    fs = config_handler_resource.get_features_selected()
    assert len(fs) == 4

    fn = config_handler_resource.get_features_numerical()
    assert len(fn) == 2

    ret = config_handler_resource.next_node(result, debug=False)
    print(json.dumps(ret))

    assert ret[0] == '0'
    assert ret[1] == ''