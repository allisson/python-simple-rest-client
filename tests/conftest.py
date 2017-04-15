import pytest

from simple_rest_client.resource import BaseResource, Resource
from simple_rest_client.api import API


@pytest.fixture
def base_resource():
    return BaseResource


custom_actions = {
    'list': {
        'method': 'GET',
        'url': '{}/users'
    },
    'create': {
        'method': 'POST',
        'url': '{}/users'
    },
    'retrieve': {
        'method': 'GET',
        'url': '{}/users/{}'
    },
    'update': {
        'method': 'PUT',
        'url': '{}/users/{}'
    },
    'partial_update': {
        'method': 'PATCH',
        'url': '{}/users/{}'
    },
    'destroy': {
        'method': 'DELETE',
        'url': '{}/users/{}'
    },
}


@pytest.fixture
def actions():
    return custom_actions


class CustomResource(Resource):
    actions = custom_actions


@pytest.fixture
def custom_resource():
    return CustomResource


@pytest.fixture
def reqres_resource():
    return Resource(
        api_root_url='https://reqres.in/api/', resource_name='users',
        json_encode_body=True
    )


@pytest.fixture
def api():
    return API(api_root_url='https://reqres.in/api/', json_encode_body=True)


@pytest.fixture
def reqres_api(api):
    api.add_resource(resource_name='users')
    api.add_resource(resource_name='login')
    return api
