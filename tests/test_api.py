import status

from simple_rest_client.resource import Resource
from tests.vcr import vcr


def test_api_add_resource(api, reqres_resource):
    api.add_resource(resource_name='users')
    assert isinstance(api.users, Resource)
    assert api.users.api_root_url == reqres_resource.api_root_url
    assert api.users.resource_name == reqres_resource.resource_name
    assert api.users.headers == reqres_resource.headers
    assert api.users.action_urls == reqres_resource.action_urls
    assert api.users.timeout == reqres_resource.timeout
    assert api.users.append_slash == reqres_resource.append_slash
    assert api.users.json_encode_body == reqres_resource.json_encode_body
    assert 'users' in api._resources


def test_api_add_resource_with_other_resource_class(api, reqres_resource):
    class AnotherResource(Resource):
        def extra_action(self):
            return True

    api.add_resource(resource_name='users', resource_class=AnotherResource)
    assert api.users.extra_action()


def test_api_get_resource_list(api):
    api.add_resource(resource_name='users')
    api.add_resource(resource_name='login')
    resource_list = api.get_resource_list()
    assert 'users' in resource_list
    assert 'login' in resource_list


@vcr.use_cassette()
def test_reqres_api_users_list(reqres_api):
    response = reqres_api.users.list()
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'GET'
    assert response.url == 'https://reqres.in/api/users'
    assert response.headers
    assert response.body


@vcr.use_cassette()
def test_reqres_api_users_create(reqres_api):
    body = {'name': 'morpheus', 'job': 'leader'}
    response = reqres_api.users.create(body=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.method == 'POST'
    assert response.url == 'https://reqres.in/api/users'
    assert response.headers
    assert response.body


@vcr.use_cassette()
def test_reqres_api_users_retrieve(reqres_api):
    id = 2
    response = reqres_api.users.retrieve(id)
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'GET'
    assert response.url == 'https://reqres.in/api/users/2'
    assert response.headers
    assert response.body


@vcr.use_cassette()
def test_reqres_api_users_update(reqres_api):
    id = 2
    body = {'name': 'morpheus', 'job': 'janitor'}
    response = reqres_api.users.update(id, body=body)
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'PUT'
    assert response.url == 'https://reqres.in/api/users/2'
    assert response.headers
    assert response.body


@vcr.use_cassette()
def test_reqres_api_users_partial_update(reqres_api):
    id = 2
    body = {'name': 'morpheus', 'job': 'janitor'}
    response = reqres_api.users.partial_update(id, body=body)
    assert response.status_code == status.HTTP_200_OK
    assert response.method == 'PATCH'
    assert response.url == 'https://reqres.in/api/users/2'
    assert response.headers
    assert response.body


@vcr.use_cassette()
def test_reqres_api_users_destroy(reqres_api):
    id = 2
    response = reqres_api.users.destroy(id)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.method == 'DELETE'
    assert response.url == 'https://reqres.in/api/users/2'
    assert response.headers
    assert response.body == ''
