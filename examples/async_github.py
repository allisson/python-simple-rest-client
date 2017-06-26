import asyncio

from simple_rest_client.api import API
from simple_rest_client.resource import AsyncResource


class EventResource(AsyncResource):
    actions = {
        'public_events': {'method': 'GET', 'url': 'events'},
        'repository_events': {'method': 'GET', 'url': '/repos/{}/{}/events'},
        'repository_issues_events': {'method': 'GET', 'url': '/repos/{}/{}/issues/events'},
        'public_network_events': {'method': 'GET', 'url': '/networks/{}/{}/events'},
        'public_organization_events': {'method': 'GET', 'url': '/orgs/{}/events'},
        'user_received_events': {'method': 'GET', 'url': '/users/{}/received_events'},
        'public_user_received_events': {'method': 'GET', 'url': '/users/{}/received_events/public'},
        'user_events': {'method': 'GET', 'url': '/users/{}/events'},
        'public_user_events': {'method': 'GET', 'url': '/users/{}/events/public'},
        'organization_events': {'method': 'GET', 'url': '/users/{}/events/orgs/{}'},
    }


# https://github.com/settings/tokens
default_params = {'access_token': 'valid-token'}
github_api = API(
    api_root_url='https://api.github.com', params=default_params,
    json_encode_body=True
)
github_api.add_resource(resource_name='events', resource_class=EventResource)


async def main():
    print('github_api.events.public_events={!r}'.format(await github_api.events.public_events()))
    print('github_api.events.repository_events={!r}'.format(await github_api.events.repository_events('allisson', 'python-simple-rest-client')))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
