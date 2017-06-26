import pytest
import responses
from aioresponses import aioresponses

from simple_rest_client.resource import Resource


def test_api_add_resource(api, reqres_resource):
    api.add_resource(resource_name='users')
    assert isinstance(api.users, Resource)
    attrs = (
        'api_root_url', 'resource_name', 'headers', 'actions', 'timeout',
        'append_slash', 'json_encode_body'
    )
    for attr in attrs:
        assert getattr(api.users, attr) == getattr(reqres_resource, attr)
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


@pytest.mark.parametrize('url,method,status,action,args,kwargs', [
    ('https://reqres.in/api/users', 'GET', 200, 'list', None, {}),
    ('https://reqres.in/api/users', 'POST', 201, 'create', None, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'GET', 200, 'retrieve', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'PUT', 200, 'update', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'PATCH', 200, 'partial_update', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'DELETE', 204, 'destroy', 2, {'body': {'success': True}}),
])
@responses.activate
def test_reqres_api_users_actions(url, method, status, action, args, kwargs, reqres_api):
    responses.add(
        getattr(responses, method),
        url,
        json={'success': True},
        status=status
    )

    response = getattr(reqres_api.users, action)(args, **kwargs)
    assert response.status_code == status
    assert response.method == method
    assert response.url == url
    assert response.body == {'success': True}


@pytest.mark.asyncio
@pytest.mark.parametrize('url,method,status,action,args,kwargs', [
    ('https://reqres.in/api/users', 'GET', 200, 'list', None, {}),
    ('https://reqres.in/api/users', 'POST', 201, 'create', None, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'GET', 200, 'retrieve', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'PUT', 200, 'update', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'PATCH', 200, 'partial_update', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'DELETE', 204, 'destroy', 2, {'body': {'success': True}}),
])
async def test_reqres_async_api_users_actions(url, method, status, action, args, kwargs, reqres_async_api):
    with aioresponses() as mock_response:
        mock_response_method = getattr(mock_response, method.lower())
        mock_response_method(url, status=status, body=b'{"success": true}', headers={'Content-Type': 'application/json'})
        response = await getattr(reqres_async_api.users, action)(args, **kwargs)
    assert response.status_code == status
    assert response.method == method
    assert response.url == url
    assert response.body == {'success': True}
