from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class UserResource(Resource):
    actions = {
        'search': {'method': 'GET', 'url': 'users/search'},
        'retrieve': {'method': 'GET', 'url': 'users/{}'},
        'retrieve_media': {'method': 'GET', 'url': 'users/{}/media/recent'},
        'retrieve_likes': {'method': 'GET', 'url': 'users/self/media/recent'}
    }


# https://www.slickremix.com/docs/how-to-create-instagram-access-token/
# get token with public_content scope
default_params = {'access_token': 'valid-token'}
instagram_api = API(
    api_root_url='https://api.instagram.com/v1/', params=default_params,
    json_encode_body=True
)
instagram_api.add_resource(resource_name='users', resource_class=UserResource)
print('instagram_api.users.search={!r}'.format(instagram_api.users.search(params={'q': 'allissonazevedo'}).body))
print('instagram_api.users.retrieve={!r}'.format(instagram_api.users.retrieve('self').body))
print('instagram_api.users.retrieve_media={!r}'.format(instagram_api.users.retrieve_media('self').body))
print('instagram_api.users.retrieve_likes={!r}'.format(instagram_api.users.retrieve_likes().body))
