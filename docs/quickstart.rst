Quickstart
==========

Let's start building a client for users resource in https://reqres.in/ service::
    
    >>> from simple_rest_client.api import API
    >>> api = API(
    ...     api_root_url='https://reqres.in/api/', # base api url
    ...     params={}, # default params
    ...     headers={}, # default headers
    ...     timeout=2, # default timeout in seconds
    ...     append_slash=False, # append slash to final url
    ...     json_encode_body=True, # encode body as json
    ... )
    >>> api.add_resource(resource_name='users') # add users resource
    >>> api.users.actions # show resource actions 
    {'list': {'method': 'GET', 'url': 'users'}, 'create': {'method': 'POST', 'url': 'users'}, 'retrieve': {'method': 'GET', 'url': 'users/{}'}, 'update': {'method': 'PUT', 'url': 'users/{}'}, 'partial_update': {'method': 'PATCH', 'url': 'users/{}'}, 'destroy': {'method': 'DELETE', 'url': 'users/{}'}} 
    >>> response = api.users.list(body=None, params={}, headers={}) # list action
    >>> response.url
    'https://reqres.in/api/users'
    >>> response.method
    'GET'
    >>> response.body
    {'page': 1, 'per_page': 3, 'total': 12, 'total_pages': 4, 'data': [{'id': 1, 'first_name': 'george', 'last_name': 'bluth', 'avatar': 'https://s3.amazonaws.com/uifaces/faces/twitter/calebogden/128.jpg'}, {'id': 2, 'first_name': 'lucille', 'last_name': 'bluth', 'avatar': 'https://s3.amazonaws.com/uifaces/faces/twitter/josephstein/128.jpg'}, {'id': 3, 'first_name': 'oscar', 'last_name': 'bluth', 'avatar': 'https://s3.amazonaws.com/uifaces/faces/twitter/olegpogodaev/128.jpg'}]}
    >>> response.headers
    {'Date': 'Sat, 15 Apr 2017 21:39:46 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'X-Powered-By': 'Express', 'Access-Control-Allow-Origin': '*', 'ETag': 'W/"1be-q96WkDv6JqfLvIPiRhzWJQ"', 'Server': 'cloudflare-nginx', 'CF-RAY': '35020f33aaf04a9c-GRU', 'Content-Encoding': 'gzip'}
    >>> response.status_code
    200
    >>> body = {'name': 'morpheus', 'job': 'leader'}
    >>> response = api.users.create(body=body, params={}, headers={}) # create action
    >>> response.status_code
    201
    >>> response = api.users.retrieve(2, body=None, params={}, headers={}) # retrieve action
    >>> response.status_code
    200
    >>> response = api.users.update(2, body=body, params={}, headers={}) # update action
    >>> response.status_code
    200
    >>> response = api.users.partial_update(2, body=body, params={}, headers={}) # partial update action
    >>> response.status_code
    200
    >>> response = api.users.destroy(2, body=None, params={}, headers={}) # destroy action
    >>> response.status_code
    204


