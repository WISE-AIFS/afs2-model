import os

import pytest

from afs.clients.models import Model


@pytest.fixture(scope='module')
def model_repository(instance):
    manifest = {
        'name': 'sdk_models_test_fixture'
    }

    model_repository = instance.model_repositories.create(**manifest)
    yield model_repository

    model_repository.delete()


@pytest.fixture(scope='module')
def models_client(model_repository):
    yield model_repository.models


@pytest.fixture()
def model_path():
    model_path = os.path.join(os.path.dirname(__file__), 'model_fixture')
    with open(model_path, 'w') as f:
        f.write('model_fixture')

    yield model_path

    os.remove(model_path)


@pytest.fixture()
def model(models_client, model_path):
    manifest = {
        'name': 'sdk_models_test_fixture',
        'model_path': model_path
    }

    model = models_client.create(**manifest)
    yield model

    try:
        model.delete()
    except:
        pass


@pytest.fixture()
def model_id(model):
    yield model.uuid


@pytest.fixture()
def remove_all_models(models_client):

    yield

    for model in models_client():
        model.delete()


def test_list_models(models_client):

    models = models_client()
    assert isinstance(models, list)
    assert len(models) == 0


# Parametrized needed
def test_create_model(models_client, model_path, remove_all_models):

    manifest = {
        'name': 'sdk_model_create_test',
        'model_path': model_path
    }
    model = models_client.create(**manifest)
    assert isinstance(model, dict)
    assert isinstance(model, Model)


def test_get_model(models_client, model_id):

    model = models_client(model_id)
    assert isinstance(model, dict)
    assert isinstance(model, Model)

    model = models_client(uuid=model_id)
    assert isinstance(model, dict)
    assert isinstance(model, Model)

    model = models_client.get(model_id)
    assert isinstance(model, dict)
    assert isinstance(model, Model)

    model = models_client.get(uuid=model_id)
    assert isinstance(model, dict)
    assert isinstance(model, Model)

    assert isinstance(model.uuid, str)
    assert model.uuid == model_id

    assert isinstance(model.name, str)
    assert isinstance(model.binary, bytes)


def test_download_model(model, model_path):
    os.remove(model_path)
    download_result = model.download(model_path)
    assert download_result


def test_update_model_by_id(models_client, model_id):
    with pytest.raises(NotImplementedError) as excinfo:
        models_client.update(model_id)


def test_update_model(model):
    with pytest.raises(NotImplementedError) as excinfo:
        model.update()


def test_delete_model_by_id(models_client, model_id):
    delete_result = models_client.delete(model_id)
    assert delete_result == {}


def test_delete_model(model):
    delete_result = model.delete()
    assert delete_result == {}
