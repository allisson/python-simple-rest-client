import pytest
import responses
from aioresponses import aioresponses

from simple_rest_client.exceptions import ActionNotFound, ActionURLMatchError


def test_base_resource_actions(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users')
    assert resource.actions == resource.default_actions


def test_base_resource_get_action_full_url(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users')
    assert resource.get_action_full_url('list') == 'http://example.com/users'
    assert resource.get_action_full_url('create') == 'http://example.com/users'
    assert resource.get_action_full_url('retrieve', 1) == 'http://example.com/users/1'
    assert resource.get_action_full_url('update', 1) == 'http://example.com/users/1'
    assert resource.get_action_full_url('partial_update', 1) == 'http://example.com/users/1'
    assert resource.get_action_full_url('destroy', 1) == 'http://example.com/users/1'


def test_base_resource_get_action_full_url_with_append_slash(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users', append_slash=True)
    assert resource.get_action_full_url('list') == 'http://example.com/users/'
    assert resource.get_action_full_url('create') == 'http://example.com/users/'
    assert resource.get_action_full_url('retrieve', 1) == 'http://example.com/users/1/'
    assert resource.get_action_full_url('update', 1) == 'http://example.com/users/1/'
    assert resource.get_action_full_url('partial_update', 1) == 'http://example.com/users/1/'
    assert resource.get_action_full_url('destroy', 1) == 'http://example.com/users/1/'


def test_base_resource_get_action_full_url_with_action_not_found(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users')
    with pytest.raises(ActionNotFound) as execinfo:
        resource.get_action_full_url('notfoundaction')
    assert 'action "notfoundaction" not found' in str(execinfo)


def test_base_resource_get_action_full_url_with_action_url_match_error(base_resource):
    resource = base_resource(api_root_url='http://example.com', resource_name='users')
    with pytest.raises(ActionURLMatchError) as execinfo:
        resource.get_action_full_url('retrieve')
    assert 'No url match for "retrieve"' in str(execinfo)


def test_custom_resource_actions(custom_resource, actions):
    resource = custom_resource(api_root_url='http://example.com', resource_name='users')
    assert resource.actions == actions


def test_custom_resource_get_action_full_url(custom_resource):
    resource = custom_resource(api_root_url='http://example.com', resource_name='users')
    assert resource.get_action_full_url('list', 1) == 'http://example.com/1/users'
    assert resource.get_action_full_url('create', 1) == 'http://example.com/1/users'
    assert resource.get_action_full_url('retrieve', 1, 2) == 'http://example.com/1/users/2'
    assert resource.get_action_full_url('update', 1, 2) == 'http://example.com/1/users/2'
    assert resource.get_action_full_url('partial_update', 1, 2) == 'http://example.com/1/users/2'
    assert resource.get_action_full_url('destroy', 1, 2) == 'http://example.com/1/users/2'


@pytest.mark.parametrize('url,method,status,action,args,kwargs', [
    ('https://reqres.in/api/users', 'GET', 200, 'list', None, {}),
    ('https://reqres.in/api/users', 'POST', 201, 'create', None, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'GET', 200, 'retrieve', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'PUT', 200, 'update', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'PATCH', 200, 'partial_update', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'DELETE', 204, 'destroy', 2, {'body': {'success': True}}),
])
@responses.activate
def test_resource_actions(url, method, status, action, args, kwargs, reqres_resource):
    responses.add(
        getattr(responses, method),
        url,
        json={'success': True},
        status=status
    )

    response = getattr(reqres_resource, action)(args, **kwargs)
    assert response.status_code == status
    assert response.method == method
    assert response.url == url
    assert response.body == {'success': True}


@pytest.mark.parametrize('content_type,response_body,expected_response_body', [
    ('application/json', '{"success": true}', {'success': True}),
    ('application/json', '', ''),
    ('text/plain', '{"success": true}', '{"success": true}'),
    ('application/octet-stream', '{"success": true}', b'{"success": true}'),
])
@responses.activate
def test_resource_response_body(content_type, response_body, expected_response_body, reqres_resource):
    url = 'https://reqres.in/api/users'
    responses.add(
        responses.GET,
        url,
        body=response_body,
        status=200,
        content_type=content_type
    )

    response = reqres_resource.list()
    assert response.body == expected_response_body


@pytest.mark.asyncio
@pytest.mark.parametrize('url,method,status,action,args,kwargs', [
    ('https://reqres.in/api/users', 'GET', 200, 'list', None, {}),
    ('https://reqres.in/api/users', 'POST', 201, 'create', None, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'GET', 200, 'retrieve', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'PUT', 200, 'update', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'PATCH', 200, 'partial_update', 2, {'body': {'success': True}}),
    ('https://reqres.in/api/users/2', 'DELETE', 204, 'destroy', 2, {'body': {'success': True}}),
])
async def test_async_resource_actions(url, method, status, action, args, kwargs, reqres_async_resource):
    with aioresponses() as mock_response:
        mock_response_method = getattr(mock_response, method.lower())
        mock_response_method(url, status=status, body=b'{"success": true}', headers={'Content-Type': 'application/json'})
        response = await getattr(reqres_async_resource, action)(args, **kwargs)
    assert response.status_code == status
    assert response.method == method
    assert response.url == url
    assert response.body == {'success': True}


@pytest.mark.asyncio
@pytest.mark.parametrize('content_type,response_body,expected_response_body', [
    ('application/json', '{"success": true}', {'success': True}),
    ('application/json', '', ''),
    ('text/plain', '{"success": true}', '{"success": true}'),
    ('application/octet-stream', '{"success": true}', b'{"success": true}'),
])
async def test_asyncresource_response_body(content_type, response_body, expected_response_body, reqres_async_resource):
    url = 'https://reqres.in/api/users'
    with aioresponses() as mock_response:
        mock_response.get(url, status=200, body=response_body, headers={'Content-Type': content_type})
        response = await reqres_async_resource.list()
    assert response.body == expected_response_body
