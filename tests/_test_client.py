import os


def test_login(client_session):
    target_endpoint = ''
    username = ''
    password = ''

    client_session.login(target_endpoint, username, password)

    assert client_session.target_endpoint == 'https://' + target_endpoint
    assert client_session.api_version == 'v1'


def test_list_service_instances(client_session):
    service_instances = client_session.list_service_instances()

    assert isinstance(service_instances, list)


def test_target(client_session):
    service_instance_id = client_session.list_service_instances()[0]

    client_session.target(service_instance_id)

    assert client_session.service_instance_id == service_instance_id
    assert isinstance(client_session.auth_code, str)
    assert len(client_session.auth_code) == 22

    assert isinstance(client_session.endpoints, dict)
    assert 'workspace_endpoint' in client_session.endpoints.keys()
    assert os.path.join('/', client_session.api_version, service_instance_id, 'workspaces') in client_session.endpoints['workspace_endpoint']

    assert 'catalog_endpoint' in client_session.endpoints.keys()
    assert client_session.endpoints['catalog_endpoint'].endswith(os.path.join('/', client_session.api_version, service_instance_id, 'catalog'))

    assert 'tasks_edpoint' in client_session.endpoints.keys()
    assert client_session.endpoints['tasks_edpoint'].endswith(os.path.join('/', client_session.api_version, service_instance_id, 'tasks'))

    assert 'models_endpoint' in client_session.endpoints.keys()
    assert client_session.endpoints['models_endpoint'].endswith(os.path.join('/', client_session.api_version, service_instance_id, 'models'))


# TODO: Add push test