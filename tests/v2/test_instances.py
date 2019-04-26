import pytest

from afs2_model.clients.instances import Instance
from afs2_model.clients.model_repositories import ModelRpositoriesClient


def test_list_instances(afs_client):

    instances = afs_client.instances()
    assert isinstance(instances, list)
    assert len(instances) > 0

    # With pagniation
    instances = afs_client.instances(limit=1)
    assert isinstance(instances, list)
    assert len(instances) == 1

    instance = instances[0]
    assert isinstance(instance, dict)
    assert isinstance(instance, Instance)


def test_get_instance(afs_client, instance_id):

    instance = afs_client.instances(instance_id)
    assert isinstance(instance, dict)
    assert isinstance(instance, Instance)

    instance = afs_client.instances(uuid=instance_id)
    assert isinstance(instance, dict)
    assert isinstance(instance, Instance)

    instance = afs_client.instances.get(instance_id)
    assert isinstance(instance, dict)
    assert isinstance(instance, Instance)

    instance = afs_client.instances.get(uuid=instance_id)
    assert isinstance(instance, dict)
    assert isinstance(instance, Instance)

    # assert for instance.uuid
    assert isinstance(instance.uuid, str)

    assert isinstance(instance.resource, str)
    assert instance.resource == "instance"

    assert isinstance(instance.api_endpoint, str)
    assert instance.api_endpoint.startswith("https://")

    model_repositories_client = getattr(instance, "model_repositories")
    assert isinstance(model_repositories_client, ModelRpositoriesClient)


def test_create_instance(afs_client):
    with pytest.raises(NotImplementedError) as excinfo:
        afs_client.instances.create()


def test_update_instance_by_id(afs_client, instance_id):
    with pytest.raises(NotImplementedError) as excinfo:
        afs_client.instances.update(instance_id)


def test_update_instance(afs_client, instance):
    with pytest.raises(NotImplementedError) as excinfo:
        instance.update()


def test_delete_instance_by_id(afs_client, instance_id):
    with pytest.raises(NotImplementedError) as excinfo:
        afs_client.instances.delete(instance_id)


def test_delete_instance(afs_client, instance):
    with pytest.raises(NotImplementedError) as excinfo:
        instance.delete()
