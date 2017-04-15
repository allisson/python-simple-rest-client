from unittest import mock

import pytest
from requests.exceptions import (
    Timeout, ConnectionError as RequestsConnectionError
)

from simple_rest_client.decorators import (
    handle_request_error, validate_response
)
from simple_rest_client.exceptions import (
    ClientConnectionError, ClientError, ServerError
)
from simple_rest_client.models import Response


@pytest.mark.parametrize('status_code', range(500, 506))
def test_validate_response_server_error(status_code):
    response = Response(
        url='http://example.com', method='GET', body=None, headers={},
        status_code=status_code
    )
    with pytest.raises(ServerError):
        validate_response(response)


@pytest.mark.parametrize('status_code', range(400, 417))
def test_validate_response_client_error(status_code):
    response = Response(
        url='http://example.com', method='GET', body=None, headers={},
        status_code=status_code
    )
    with pytest.raises(ClientError):
        validate_response(response)


@pytest.mark.parametrize('side_effect', (Timeout, RequestsConnectionError))
def test_handle_request_error_exceptions(side_effect):
    wrapped = mock.Mock(side_effect=side_effect)
    with pytest.raises(ClientConnectionError):
        handle_request_error(wrapped)()
