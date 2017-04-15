from functools import wraps
import logging

from requests.exceptions import (
    Timeout, ReadTimeout, ConnectionError as RequestsConnectionError
)
import status

from simple_rest_client.exceptions import (
    ClientConnectionError, ClientError, ServerError
)

logger = logging.getLogger(__name__)


def validate_response(response):
    error_suffix = ' response={!r}'.format(response)
    if status.is_client_error(code=response.status_code):
        raise ClientError('operation=client_error,' + error_suffix, response)
    if status.is_server_error(code=response.status_code):
        raise ServerError('operation=server_error,' + error_suffix, response)


def handle_request_error(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
        except (Timeout, ReadTimeout, RequestsConnectionError) as exc:
            logger.exception(exc)
            raise ClientConnectionError() from exc

        validate_response(response)

        return response

    return wrapper
