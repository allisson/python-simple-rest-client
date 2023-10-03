import asyncio

from simple_rest_client.api import API
from simple_rest_client.resource import AsyncResource


class BasicAuthResource(AsyncResource):
    actions = {"retrieve": {"method": "GET", "url": "basic-auth/{}/{}"}}


# https://httpbin.org/
auth = ("username", "password")
httpbin_api = API(api_root_url="https://httpbin.org/", ssl_verify=False)
httpbin_api.add_resource(resource_name="basic_auth", resource_class=BasicAuthResource)


async def main():
    response = await httpbin_api.basic_auth.retrieve("username", "password", auth=auth)
    print("httpbin_api.basic_auth.retrieve={!r}".format(response.body))
    await httpbin_api.aclose_client()


asyncio.run(main())
