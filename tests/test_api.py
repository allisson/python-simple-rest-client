import pytest

from simple_rest_client.api import API
from simple_rest_client.resource import Resource


def test_api_headers():
    api = API(api_root_url="http://localhost:0/api/")
    assert api.headers == {}

    json_api = API(api_root_url="http://localhost:0/api/", headers={"Content-Type": "application/json"})
    assert json_api.headers == {"Content-Type": "application/json"}


@pytest.mark.parametrize("ssl_verify,expected_ssl_verify", [(None, True), (True, True), (False, False)])
def test_api_ssl_verify(ssl_verify, expected_ssl_verify, api, reqres_resource):
    api = API(api_root_url="http://localhost:0/api/", json_encode_body=True, ssl_verify=ssl_verify)
    api.add_resource(resource_name="users")
    assert api.ssl_verify == expected_ssl_verify


def test_api_add_resource(api, reqres_resource):
    api.add_resource(resource_name="users")
    assert isinstance(api.users, Resource)
    attrs = (
        "actions",
        "api_root_url",
        "append_slash",
        "headers",
        "json_encode_body",
        "resource_name",
        "ssl_verify",
        "timeout",
    )
    for attr in attrs:
        assert getattr(api.users, attr) == getattr(reqres_resource, attr)
    assert "users" in api._resources


@pytest.mark.parametrize(
    "resource_name,resource_valid_name",
    [("users", "users"), ("my-users", "my_users"), ("my users", "my_users"), ("影師嗎", "ying_shi_ma")],
)
def test_api_resource_valid_name(resource_name, resource_valid_name, api):
    api.add_resource(resource_name=resource_name)
    resource = getattr(api, resource_valid_name)
    assert isinstance(resource, Resource)
    assert resource_valid_name in api._resources


def test_api_add_resource_with_other_resource_class(api, reqres_resource):
    class AnotherResource(Resource):
        def extra_action(self):
            return True

    api.add_resource(resource_name="users", resource_class=AnotherResource)
    assert api.users.extra_action()


def test_api_get_resource_list(api):
    api.add_resource(resource_name="users")
    api.add_resource(resource_name="login")
    resource_list = api.get_resource_list()
    assert "users" in resource_list
    assert "login" in resource_list


@pytest.mark.parametrize(
    "url,method,status,action,args,kwargs",
    [
        ("/api/users", "GET", 200, "list", None, {}),
        ("/api/users", "POST", 201, "create", None, {"body": {"success": True}}),
        ("/api/users/2", "GET", 200, "retrieve", 2, {"body": {"success": True}}),
        ("/api/users/2", "PUT", 200, "update", 2, {"body": {"success": True}}),
        ("/api/users/2", "PATCH", 200, "partial_update", 2, {"body": {"success": True}}),
        ("/api/users/2", "DELETE", 204, "destroy", 2, {"body": {"success": True}}),
    ],
)
def test_reqres_api_users_actions(httpserver, url, method, status, action, args, kwargs, reqres_api):
    httpserver.expect_request(url, method=method).respond_with_json({"success": True}, status=status)

    response = getattr(reqres_api.users, action)(args, **kwargs)
    assert response.status_code == status
    assert response.method == method
    assert url in response.url
    if method != "DELETE":
        assert response.body == {"success": True}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "url,method,status,action,args,kwargs",
    [
        ("/api/users", "GET", 200, "list", None, {}),
        ("/api/users", "POST", 201, "create", None, {"body": {"success": True}}),
        ("/api/users/2", "GET", 200, "retrieve", 2, {"body": {"success": True}}),
        ("/api/users/2", "PUT", 200, "update", 2, {"body": {"success": True}}),
        ("/api/users/2", "PATCH", 200, "partial_update", 2, {"body": {"success": True}}),
        ("/api/users/2", "DELETE", 204, "destroy", 2, {"body": {"success": True}}),
    ],
)
async def test_reqres_async_api_users_actions(
    httpserver, url, method, status, action, args, kwargs, reqres_async_api
):
    httpserver.expect_request(url, method=method).respond_with_json({"success": True}, status=status)

    response = await getattr(reqres_async_api.users, action)(args, **kwargs)
    assert response.status_code == status
    assert response.method == method
    assert url in response.url
    if method != "DELETE":
        assert response.body == {"success": True}
