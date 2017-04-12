import pytest
import status

from tests.vcr import vcr


def test_base_resource_default_action_urls(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users')
    assert resource.action_urls == {
        'list': 'users',
        'create': 'users',
        'retrieve': 'users/{}',
        'update': 'users/{}',
        'partial_update': 'users/{}',
        'destroy': 'users/{}'
    }


def test_base_resource_set_action_urls(base_resource, action_urls):
    resource = base_resource(api_root_url='http://example.com', resource_name='users', action_urls=action_urls)
    assert resource.action_urls == action_urls


def test_base_resource_get_full_url(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users')
    assert resource.get_full_url('list') == 'http://example.com/users'
    assert resource.get_full_url('create') == 'http://example.com/users'
    assert resource.get_full_url('retrieve', 1) == 'http://example.com/users/1'
    assert resource.get_full_url('update', 1) == 'http://example.com/users/1'
    assert resource.get_full_url('partial_update', 1) == 'http://example.com/users/1'
    assert resource.get_full_url('destroy', 1) == 'http://example.com/users/1'


def test_base_resource_get_full_url_with_set_action_urls(base_resource, action_urls):
    resource = base_resource(api_root_url='http://example.com', resource_name='users', action_urls=action_urls)
    assert resource.get_full_url('list', 1) == 'http://example.com/1/users'
    assert resource.get_full_url('create', 1) == 'http://example.com/1/users'
    assert resource.get_full_url('retrieve', 1, 2) == 'http://example.com/1/users/2'
    assert resource.get_full_url('update', 1, 2) == 'http://example.com/1/users/2'
    assert resource.get_full_url('partial_update', 1, 2) == 'http://example.com/1/users/2'
    assert resource.get_full_url('destroy', 1, 2) == 'http://example.com/1/users/2'


def test_base_resource_get_full_url_with_append_slash(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users', append_slash=True)
    assert resource.get_full_url('list') == 'http://example.com/users/'
    assert resource.get_full_url('create') == 'http://example.com/users/'
    assert resource.get_full_url('retrieve', 1) == 'http://example.com/users/1/'
    assert resource.get_full_url('update', 1) == 'http://example.com/users/1/'
    assert resource.get_full_url('partial_update', 1) == 'http://example.com/users/1/'
    assert resource.get_full_url('destroy', 1) == 'http://example.com/users/1/'


def test_base_resource_get_full_url_with_invalid_action(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users')
    with pytest.raises(ValueError) as execinfo:
        resource.get_full_url('listy')
    assert 'No url match for "listy"' in str(execinfo)


@vcr.use_cassette()
def test_resource_list(reqres_resource):
    response = reqres_resource.list()
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'GET'
    assert response.url == 'https://reqres.in/api/users'
    assert response.headers
    assert response.body


@vcr.use_cassette()
def test_resource_create(reqres_resource):
    body = {'name': 'morpheus', 'job': 'leader'}
    response = reqres_resource.create(body=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.method == 'POST'
    assert response.url == 'https://reqres.in/api/users'
    assert response.headers
    assert response.body


@vcr.use_cassette()
def test_resource_retrieve(reqres_resource):
    id = 2
    response = reqres_resource.retrieve(id)
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'GET'
    assert response.url == 'https://reqres.in/api/users/2'
    assert response.headers
    assert response.body


@vcr.use_cassette()
def test_resource_update(reqres_resource):
    id = 2
    body = {'name': 'morpheus', 'job': 'zion resident'}
    response = reqres_resource.update(id, body=body)
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'PUT'
    assert response.url == 'https://reqres.in/api/users/2'
    assert response.headers
    assert response.body


@vcr.use_cassette()
def test_resource_partial_update(reqres_resource):
    id = 2
    body = {'name': 'morpheus', 'job': 'zion resident'}
    response = reqres_resource.partial_update(id, body=body)
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'PATCH'
    assert response.url == 'https://reqres.in/api/users/2'
    assert response.headers
    assert response.body


@vcr.use_cassette()
def test_resource_destroy(reqres_resource):
    id = 2
    response = reqres_resource.destroy(id)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.method == 'DELETE'
    assert response.url == 'https://reqres.in/api/users/2'
    assert response.headers
    assert response.body == ''
