import os
import json
import pytest

def test_services_influxdb(services_resource):
    services = services_resource.get_service_list()

    assert len(services) != 0

def test_services_specific_key(services_resource):
    services = services_resource.get_service_info('influxdb')

    assert 'username' in services
    assert 'password' in services
    assert 'database' in services
    assert 'host' in services

def test_services_key_not_exist(services_resource):

    with pytest.raises(Exception):
        pytest.raises(services_resource.get_service_info('influxdb'))

    assert len(services_resource.get_service_info('influxdb', service_key='123')) == 0
