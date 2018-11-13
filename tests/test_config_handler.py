import json
import os

def test_config_handler_para_feature_data(mocker, config_handler_resource, data_dir, capsys):
    config_handler_resource.set_param('myinteger', type='integer', required=True, default=2)
    config_handler_resource.set_param('myfloat', type='float', required=True, default=2.345)
    config_handler_resource.set_param('mystring', type='string', required=True, default='ms')
    config_handler_resource.set_param('mylist', type='list', required=True, default=['a','b'])
    config_handler_resource.set_features(True)
    config_handler_resource.set_column('mycolumn')
    config_handler_resource.summary()

    out, err = capsys.readouterr()
    expect_out = {
        'features':
        True,
        'param': [{
            'name': 'myinteger',
            'type': 'integer',
            'required': True,
            'default': 2
        }, {
            'name': 'myfloat',
            'type': 'float',
            'required': True,
            'default': 2.345
        }, {
            'name': 'mystring',
            'type': 'string',
            'required': True,
            'default': 'ms'
        }, {
            'name': 'mylist',
            'type': 'list',
            'required': True,
            'default': ['a', 'b']
        }],
        'column': ['mycolumn']
    }
    assert json.loads(out) == expect_out

    with open(os.path.join(data_dir, 'config_handler_request.json'), 'r') as f:
        REQUEST = f.read()

    with open(os.path.join(data_dir, 'flow_json.json'), 'r') as f:
        flow_json = f.read()

    config_handler_resource.set_kernel_gateway(REQUEST, flow_json_file=flow_json)

    assert os.getenv("afs_url", None) ==  "https://portal-afs-develop.iii-cflab.com/"
    assert os.getenv("instance_id", None) == "456"
    assert os.getenv("auth_code", None) == "789"
    assert os.getenv("workspace_id", None) == "abc"
    assert os.getenv("node_host_url", None) == "def"

    mi = config_handler_resource.get_param('myinteger')
    mf = config_handler_resource.get_param('myfloat')
    ms = config_handler_resource.get_param('mystring')
    ml = config_handler_resource.get_param('mylist')
    data = config_handler_resource.get_data()
    column = config_handler_resource.get_column()
    assert isinstance(mi, int)
    assert mi == 2
    assert isinstance(mf, float)
    assert mf == 2.123
    assert isinstance(ms, str)
    assert ms == "abcde"
    assert isinstance(ml, list)
    assert ml == ["abc", "def", "ghi"]
    assert data['mycolumn'][0] == 21
    result = data*2
    assert column == {'mc': 'mycolumn'}

    ft = config_handler_resource.get_features_target()
    assert isinstance(ft, str)

    fs = config_handler_resource.get_features_selected()
    assert isinstance(list(fs), list)

    fn = config_handler_resource.get_features_numerical()
    assert isinstance(list(fn), list)

    mock_method = mocker.patch.object(config_handler_resource, 'get_column')

    ret = config_handler_resource.next_node(result, debug=False)
    assert mock_method.called

    # print(json.dumps(ret))
    #
    # assert ret[0] == '0'
    # assert ret[1] == ''
