from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class BasicAuthResource(Resource):
    actions = {
        'retrieve': {'method': 'GET', 'url': 'basic-auth/{}/{}'},
    }


# https://httpbin.org/
auth = ('username', 'password')
httpbin_api = API(api_root_url='https://httpbin.org/')
httpbin_api.add_resource(resource_name='basic_auth', resource_class=BasicAuthResource)
print('httpbin_api.basic_auth.retrieve={!r}'.format(httpbin_api.basic_auth.retrieve('username', 'password', auth=auth).body))
