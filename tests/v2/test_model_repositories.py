import pytest
from afs.clients.model_repositories import ModelRepository


@pytest.fixture(scope='module')
def model_repositories_client(instance):
    yield instance.model_repositories


@pytest.fixture()
def model_repo_name():
    yield 'sdk_model_repo_test_fixture'


@pytest.fixture()
def model_repository(model_repositories_client, model_repo_name):
    manifest = {
        'name': model_repo_name
    }

    model_repository = model_repositories_client.create(**manifest)
    yield model_repository

    # Use try catch to ensure this fuxture worked at delete related functions
    try:
        model_repository.delete()
    except:
        pass


@pytest.fixture()
def model_repository_id(model_repository):
    yield model_repository.uuid


@pytest.fixture()
def remove_model_repository(model_repositories_client, model_repo_name):

    yield

    for model_repository in model_repositories_client():
        if model_repository.name == model_repo_name:
            model_repository.delete()


def test_list_model_repositories(model_repositories_client):

    model_repositories = model_repositories_client()
    assert isinstance(model_repositories, list)
    assert len(model_repositories) == 0


def test_create_model_repository(model_repositories_client, model_repo_name, remove_model_repository):

    model_repository = model_repositories_client.create(name=model_repo_name)
    assert isinstance(model_repository, dict)
    assert isinstance(model_repository, ModelRepository)


def test_get_model_repository(model_repositories_client, model_repository_id):

    model_repository = model_repositories_client(model_repository_id)
    assert isinstance(model_repository, dict)
    assert isinstance(model_repository, ModelRepository)

    model_repository = model_repositories_client(uuid=model_repository_id)
    assert isinstance(model_repository, dict)
    assert isinstance(model_repository, ModelRepository)

    model_repository = model_repositories_client.get(model_repository_id)
    assert isinstance(model_repository, dict)
    assert isinstance(model_repository, ModelRepository)

    model_repository = model_repositories_client.get(uuid=model_repository_id)
    assert isinstance(model_repository, dict)
    assert isinstance(model_repository, ModelRepository)

    assert isinstance(model_repository.uuid, str)
    assert model_repository.uuid == model_repository_id

    assert isinstance(model_repository.name, str)


def test_update_model_repository_by_id(model_repositories_client, model_repository_id):
    with pytest.raises(NotImplementedError) as excinfo:
        model_repositories_client.update(model_repository_id)


def test_update_model_repository(model_repositories_client, model_repository):
    with pytest.raises(NotImplementedError) as excinfo:
        model_repository.update()


def test_delete_model_repository_by_id(model_repositories_client, model_repository_id):
    delete_result = model_repositories_client.delete(model_repository_id)
    assert delete_result == {}


def test_delete_model_repository(model_repositories_client, model_repository):
    delete_result = model_repository.delete()
    assert delete_result == {}
