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


.. |TravisCI Build Status| image:: https://travis-ci.org/allisson/python-simple-rest-client.svg?branch=master
   :target: https://travis-ci.org/allisson/python-simple-rest-client
.. |Coverage Status| image:: https://coveralls.io/repos/github/georgeyk/loafer/badge.svg?branch=master
   :target: https://coveralls.io/github/georgeyk/loafer?branch=master
.. |Requirements Status| image:: https://requires.io/github/georgeyk/loafer/requirements.svg?branch=master
   :target: https://requires.io/github/georgeyk/loafer/requirements/?branch=master
.. |Scrutinizer Code Quality| image:: https://scrutinizer-ci.com/g/georgeyk/loafer/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/georgeyk/loafer/?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/georgeyk/loafer/badges/gpa.svg
   :target: https://codeclimate.com/github/georgeyk/loafer
