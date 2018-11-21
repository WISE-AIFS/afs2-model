import json
import os

import pytest

from afs import config_handler

# def test_config_handler_catalog(mocker, config_handler_resource, data_dir, capsys):
#     config_handler_resource.set_param('myinteger', type='integer', required=True, default=2)
#     config_handler_resource.set_param('myfloat', type='float', required=True, default=2.345)
#     config_handler_resource.set_param('mystring', type='string', required=True, default='ms')
#     config_handler_resource.set_param('mylist', type='list', required=True, default=['a','b'])
#     config_handler_resource.set_features(True)
#     config_handler_resource.set_column('mycolumn')
#     config_handler_resource.summary()
#
#     out, err = capsys.readouterr()
#     expect_out = {
#         'features':
#         True,
#         'param': [{
#             'name': 'myinteger',
#             'type': 'integer',
#             'required': True,
#             'default': 2
#         }, {
#             'name': 'myfloat',
#             'type': 'float',
#             'required': True,
#             'default': 2.345
#         }, {
#             'name': 'mystring',
#             'type': 'string',
#             'required': True,
#             'default': 'ms'
#         }, {
#             'name': 'mylist',
#             'type': 'list',
#             'required': True,
#             'default': ['a', 'b']
#         }],
#         'column': ['mycolumn']
#     }
#     assert json.loads(out) == expect_out
#
#     with open(os.path.join(data_dir, 'config_handler_request_catalog.json'), 'r') as f:
#         REQUEST = f.read()
#
#     with open(os.path.join(data_dir, 'flow_json.json'), 'r') as f:
#         flow_json = f.read()
#
#     config_handler_resource.set_kernel_gateway(REQUEST, flow_json_file=flow_json)
#
#     assert os.getenv("afs_url", None) ==  "https://portal-afs-develop.iii-cflab.com/"
#     assert os.getenv("instance_id", None) == "456"
#     assert os.getenv("auth_code", None) == "789"
#     assert os.getenv("workspace_id", None) == "abc"
#     assert os.getenv("node_red_url", None) == "def"
#
#     mi = config_handler_resource.get_param('myinteger')
#     mf = config_handler_resource.get_param('myfloat')
#     ms = config_handler_resource.get_param('mystring')
#     ml = config_handler_resource.get_param('mylist')
#     data = config_handler_resource.get_data()
#     column = config_handler_resource.get_column()
#     assert isinstance(mi, int)
#     assert mi == 2
#     assert isinstance(mf, float)
#     assert mf == 2.123
#     assert isinstance(ms, str)
#     assert ms == "abcde"
#     assert isinstance(ml, list)
#     assert ml == ["abc", "def", "ghi"]
#     assert data['mycolumn'][0] == 21
#     # result = data*2
#     assert column == {'mc': 'mycolumn'}
#
#     ft = config_handler_resource.get_features_target()
#     assert isinstance(ft, str)
#
#     fs = config_handler_resource.get_features_selected()
#     assert isinstance(list(fs), list)
#
#     fn = config_handler_resource.get_features_numerical()
#     assert isinstance(list(fn), list)
#
#     # mock_method = mocker.patch.object(config_handler_resource, 'get_column')
#     # exe_next_node = mocker.patch('config_handler_resource.flow_obj.exe_next_node', return_value=['0',''])
#
#     # ret = config_handler_resource.next_node(result, debug=False)
#     # assert mock_method.called
#     # assert exe_next_node.called
#
#     # print(json.dumps(ret))
#     #
#     # assert ret[0] == '0'
#     # assert ret[1] == ''


@pytest.fixture()
def envs():
    envs = os.environ
    yield envs
    os.environ.update(envs)


@pytest.fixture()
def flow_json():
    sso_user = os.getenv('sso_user')
    sso_password = os.getenv('sso_password')
    flow_json = """{{
        "id": "2c3e36f5.79745a",
        "label": "test parser",
        "nodes": [
            {{
                "id": "1603f0e2.15482f",
                "type": "sso_setting",
                "z": "2c3e36f5.79745a",
                "name": "sso wise-paas",
                "sso_user": "{sso_user}",
                "sso_password": "{sso_password}",
                "x": 150,
                "y": 80,
                "wires": []
            }}, {{
                "id": "5da078ac.7ab548",
                "type": "firehose_influxdb_query",
                "z": "2c3e36f5.79745a",
                "name": "arfa titanic",
                "url": "",
                "_node_type": "firehose",
                "sso_token": "",
                "service_name": "influxdb_demo",
                "service_key": "influxdb_demo",
                "service_credentials": {{}},
                "feature_names": ["time", "Age", "Embarked", "Fare", "Name", "PassengerId", "Pclass", "Sex", "SibSp", "Survived"],
                "query": "select * from titanic_data",
                "x": 160,
                "y": 140,
                "wires": [
                    []
                ]
            }}, {{
                "id": "7d3b635a.f0a75c",
                "type": "test_node",
                "z": "2c3e36f5.79745a",
                "name": "test_sdk",
                "myinteger": 2,
                "myfloat": 2.123,
                "mystring": "abcde",
                "mylist": "[\\\"abc\\\", \\\"def\\\", \\\"ghi\\\"]",
                "mycolumn": "mc",
                "url": "",
                "target": "tar_1",
                "select_feature": ["sel_1", "sel_2", "sel_3", "sel_4"],
                "numerical": ["num_1", "num_2"],
                "x": 340,
                "y": 120,
                "wires": [
                    []
                ]
            }}
        ]
    }}"""

    flow_json = flow_json.format(sso_user=sso_user, sso_password=sso_password)
    yield flow_json


@pytest.fixture()
def kernel_gateway_request_workspace():
    kernel_gateway_request = """{
        "headers": {
            "Flow_id": "2c3e36f5.79745a",
            "Node_id": "7d3b635a.f0a75c"
        },
        "body": {
            "data": {
                "mc": {
                    "0": 21
                }
            }
        }
    }"""

    yield kernel_gateway_request


@pytest.fixture()
def kernel_gateway_request_catalog():
    afs_url = os.getenv('afs_url')
    kernel_gateway_request = """{{
        "headers": {{
            "Flow_id": "2c3e36f5.79745a",
            "Node_id": "7d3b635a.f0a75c",
            "Afs_url": "{afs_url}",
            "Instance_id": "456",
            "Auth_code": "789",
            "Workspace_id": "abc",
            "Node_host_url": "def"
        }},
        "body": {{
            "data": {{
                "mc": {{
                    "0": 21
                }}
            }}
        }}
    }}"""

    kernel_gateway_request = kernel_gateway_request.format(afs_url=afs_url)
    yield kernel_gateway_request


def test_config_handler_workspace(mocker, config_handler_resource, data_dir,
                                  capsys, envs, flow_json, kernel_gateway_request_workspace):
    config_handler_resource.set_param(
        'myinteger', type='integer', required=True, default=2)
    config_handler_resource.set_param(
        'myfloat', type='float', required=True, default=2.345)
    config_handler_resource.set_param(
        'mystring', type='string', required=True, default='ms')
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
        },
                  {
                      'name': 'myfloat',
                      'type': 'float',
                      'required': True,
                      'default': 2.345
                  },
                  {
                      'name': 'mystring',
                      'type': 'string',
                      'required': True,
                      'default': 'ms'
                  }],
        'column': ['mycolumn']
    }
    assert json.loads(out) == expect_out

    config_handler_resource.set_kernel_gateway(
        kernel_gateway_request_workspace, flow_json_file=flow_json)

    assert os.getenv("afs_url",) == envs['afs_url']
    assert os.getenv("instance_id") == envs['instance_id']
    assert os.getenv("auth_code") == envs['auth_code']
    assert os.getenv("workspace_id") == envs['workspace_id']
    assert os.getenv("node_red_url") == envs['node_red_url']

    mi = config_handler_resource.get_param('myinteger')
    mf = config_handler_resource.get_param('myfloat')
    ms = config_handler_resource.get_param('mystring')
    data = config_handler_resource.get_data()
    column = config_handler_resource.get_column()
    assert isinstance(mi, int)
    assert mi == 2
    assert isinstance(mf, float)
    assert mf == 2.123
    assert isinstance(ms, str)
    assert ms == "abcde"
    assert data['mycolumn'][0] == 21
    # result = data*2
    assert column == {'mc': 'mycolumn'}

    ft = config_handler_resource.get_features_target()
    assert isinstance(ft, str)

    fs = config_handler_resource.get_features_selected()
    assert isinstance(list(fs), list)

    fn = config_handler_resource.get_features_numerical()
    assert isinstance(list(fn), list)
