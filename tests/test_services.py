import os
import json
import pytest

def test_services_influxdb(services_resource):
    services = services_resource.get_service_info()

    if 'influxdb' in services:
        assert 'username' in services['influxdb'][0]
        assert 'password' in services['influxdb'][0]
        assert 'database' in services['influxdb'][0]
        assert 'host' in services['influxdb'][0]

def test_services_specific_key(services_resource):
    services = services_resource.get_service_info(specific_key='ba96b1bebce7f02115ffe9cec442e5lb')

    assert 'username' in services
    assert 'password' in services
    assert 'database' in services
    assert 'host' in services

def test_services_key_not_exist(services_resource):

    with pytest.raises(Exception):
        pytest.raises(services_resource.get_service_info(specific_key='not exist services'))

