Simple Rest Client
==================

|TravisCI Build Status| |Coverage Status| |Requirements Status|
|Scrutinizer Code Quality| |Code Climate|

----

Simple REST client for python 3.5+.


How to install
--------------

.. code:: shell

    pip install simple-rest-client


How to use
----------

.. code:: python

    >>> from simple_rest_client.api import API
    >>> api = API(api_root_url='https://reqres.in/api/', json_encode_body=True)
    >>> api.add_resource(resource_name='users')
    >>> response = api.users.list()
    >>> response.url
    'https://reqres.in/api/users'
    >>> response.method
    'GET'
    >>> response.body
    {'page': 1, 'per_page': 3, 'total': 12, 'total_pages': 4, 'data': [{'id': 1, 'first_name': 'george', 'last_name': 'bluth', 'avatar': 'https://s3.amazonaws.com/uifaces/faces/twitter/calebogden/128.jpg'}, {'id': 2, 'first_name': 'lucille', 'last_name': 'bluth', 'avatar': 'https://s3.amazonaws.com/uifaces/faces/twitter/josephstein/128.jpg'}, {'id': 3, 'first_name': 'oscar', 'last_name': 'bluth', 'avatar': 'https://s3.amazonaws.com/uifaces/faces/twitter/olegpogodaev/128.jpg'}]}
    >>> response.headers
    {'Date': 'Thu, 13 Apr 2017 10:57:02 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Set-Cookie': '__cfduid=d8352c249f38c47e35d8e21c7e3c93edc1492081022; expires=Fri, 13-Apr-18 10:57:02 GMT; path=/; domain=.reqres.in; HttpOnly', 'X-Powered-By': 'Express', 'Access-Control-Allow-Origin': '*', 'ETag': 'W/"1be-q96WkDv6JqfLvIPiRhzWJQ"', 'Server': 'cloudflare-nginx', 'CF-RAY': '34ede6f6b8ba4c3c-GRU', 'Content-Encoding': 'gzip'}
    >>> response.status_code
    200

Instagram example
-----------------

.. code:: python

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


Github example
--------------

.. code:: python

    from simple_rest_client.api import API
    from simple_rest_client.resource import Resource


    class EventResource(Resource):
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
    print('github_api.events.public_events={!r}'.format(github_api.events.public_events()))
    print('github_api.events.repository_events={!r}'.format(github_api.events.repository_events('allisson', 'python-simple-rest-client')))


.. |TravisCI Build Status| image:: https://travis-ci.org/allisson/python-simple-rest-client.svg?branch=master
   :target: https://travis-ci.org/allisson/python-simple-rest-client
.. |Coverage Status| image:: https://coveralls.io/repos/github/allisson/python-simple-rest-client/badge.svg?branch=master
   :target: https://coveralls.io/github/allisson/python-simple-rest-client?branch=master
.. |Requirements Status| image:: https://requires.io/github/allisson/python-simple-rest-client/requirements.svg?branch=master
   :target: https://requires.io/github/allisson/python-simple-rest-client/requirements/?branch=master
.. |Scrutinizer Code Quality| image:: https://scrutinizer-ci.com/g/allisson/python-simple-rest-client/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/allisson/python-simple-rest-client/?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/allisson/python-simple-rest-client/badges/gpa.svg
   :target: https://codeclimate.com/github/allisson/python-simple-rest-client
