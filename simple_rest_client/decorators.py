from functools import wraps
import logging

from requests.exceptions import Timeout, ReadTimeout, ConnectionError as RequestsConnectionError
import status

from simple_rest_client.exceptions import ClientError, ServerError

logger = logging.getLogger(__name__)


def validate_response(response):
    error_suffix = (
        ' url={}, '
        'method={}, '
        'body={!r}, '
        'headers={!r}, '
        'status_code={}'.format(
            response.url, response.method, response.body, response.headers,
            response.status_code
        )
    )
    if status.is_client_error(code=response.status_code):
        raise ClientError('operation=client_error,' + error_suffix)
    if status.is_server_error(code=response.status_code):
        raise ServerError('operation=server_error,' + error_suffix)


def handle_request_error(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
        except (Timeout, ReadTimeout, RequestsConnectionError) as exc:
            logger.exception(exc)
            raise ServerError() from exc

        validate_response(response)

        return response

    return wrapper
