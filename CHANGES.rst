Changelog
---------

1.1.3
~~~~~

* Update pre-commit config and code format.
* Remove broken examples.
* Update base requirements version.

1.1.2
~~~~~

* Fix preserve resource_name as given (thanks @leorochael).

1.1.1
~~~~~

* Fix content-type is always json if json_encode_body is true (thanks @aenima-x).

1.1.0
~~~~~

* Drop support for python 3.6.x.
* Fix json_encode_body cannot be overridden bug (thanks @denravonska).
* Replace asynctest with asyncmock.
* Update httpx and python-slugify to latest versions.
* Update pre-commit rules.

1.0.8
~~~~~

* Use httpx.RequestError as base exception for ClientConnectionError.

1.0.7
~~~~~

* Update ClientConnectionError to deal with httpx.NetworkError exceptions (thanks @depauwjimmy).

1.0.6
~~~~~

* Fix httpx exception imports on httpx 0.13.x (thanks @denravonska).

1.0.5
~~~~~

* Fix imports on httpx 0.12.x (thanks @stekman37).

1.0.4
~~~~~

* Update httpx version (sync version is back yey!).
* Use exceptions.TimeoutException for ClientConnectionError.

1.0.3
~~~~~

* Fix api resource names (thanks @cfytrok).

1.0.2
~~~~~

* Locking httpx version below 0.8.0 (thanks @patcon).

1.0.1
~~~~~

* Simplify httpx timeout handling (thanks @daneoshiga).

1.0.0
~~~~~

* Major release.
* Use httpx instead of aiohttp and requests.
* Drop python 3.5.

0.6.0
~~~~~

* Add support for disable certificate validation (thanks @rfrp).

0.5.4
~~~~~

* Prevent urls with double slashes.

0.5.3
~~~~~

* Fix api_root_url without trailing slash (thanks @dspechnikov).

0.5.2
~~~~~

* Fix JSONDecodeError when processing empty server responses (thanks @zmbbb).

0.5.1
~~~~~

* Change log level for async requests (thanks @kwarunek).

0.5.0
~~~~~

* Add new exceptions: AuthError and NotFoundError.

0.4.0
~~~~~

* Add request.kwargs support.

0.3.0
~~~~~

* Add client_response in Response object.

0.2.0
~~~~~

* Add asyncio support (aiohttp).

0.1.1
~~~~~

* Add MANIFEST.in (fix install by pip).

0.1.0
~~~~~

* Initial release.
