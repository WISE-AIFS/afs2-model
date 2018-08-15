import os
import json

def test_services_influxdb(services_resource):
    services = services_resource.get_service_info()
    assert 'influxdb' in services
    assert 'username' in services['influxdb'][0]
    assert 'password' in services['influxdb'][0]
    assert 'database' in services['influxdb'][0]
    assert 'host' in services['influxdb'][0]
