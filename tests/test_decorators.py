from unittest import mock

import pytest
from asynctest.mock import CoroutineMock
from aiohttp.client_exceptions import ServerTimeoutError
from requests.exceptions import (
    Timeout,
    ConnectionError as RequestsConnectionError
)

from simple_rest_client.decorators import (
    handle_async_request_error,
    handle_request_error,
    validate_response
)
from simple_rest_client.exceptions import (
    ClientConnectionError,
    ClientError,
    ServerError
)
from simple_rest_client.models import Response


@pytest.mark.parametrize('status_code', range(500, 506))
def test_validate_response_server_error(status_code):
    response = Response(
        url='http://example.com', method='GET', body=None, headers={},
        status_code=status_code, client_response=mock.Mock()
    )
    with pytest.raises(ServerError) as excinfo:
        validate_response(response)
    assert excinfo.value.response.status_code == status_code
    assert 'operation=server_error' in str(excinfo.value)


@pytest.mark.parametrize('status_code', range(400, 417))
def test_validate_response_client_error(status_code):
    response = Response(
        url='http://example.com', method='GET', body=None, headers={},
        status_code=status_code, client_response=mock.Mock()
    )
    with pytest.raises(ClientError) as excinfo:
        validate_response(response)
    assert excinfo.value.response.status_code == status_code
    assert 'operation=client_error' in str(excinfo.value)


@pytest.mark.parametrize('side_effect', (Timeout, RequestsConnectionError))
def test_handle_request_error_exceptions(side_effect):
    wrapped = mock.Mock(side_effect=side_effect)
    with pytest.raises(ClientConnectionError):
        handle_request_error(wrapped)()


def test_handle_async_request_error_exceptions(event_loop):
    wrapped = CoroutineMock(side_effect=ServerTimeoutError)
    with pytest.raises(ClientConnectionError):
        event_loop.run_until_complete(handle_async_request_error(wrapped)())
