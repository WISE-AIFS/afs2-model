import pytest
import uuid


@pytest.fixture()
def test():
    return uuid.uuid4()


@pytest.fixture(scope='class')
def services_resource():
    from afs import services
    afs_services=services()
    yield afs_services


@pytest.fixture(scope='function')
def config_handler_resource():
    from afs import config_handler
    afs_config_handler = config_handler()
    yield afs_config_handler