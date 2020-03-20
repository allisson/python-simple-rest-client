import logging
from functools import wraps

import httpx
import status

from .exceptions import AuthError, ClientConnectionError, ClientError, NotFoundError, ServerError

logger = logging.getLogger(__name__)


def validate_response(response):
    error_suffix = " response={!r}".format(response)
    if response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN):
        raise AuthError("operation=auth_error," + error_suffix, response)
    if response.status_code == status.HTTP_404_NOT_FOUND:
        raise NotFoundError("operation=not_found_error," + error_suffix, response)
    if status.is_client_error(code=response.status_code):
        raise ClientError("operation=client_error," + error_suffix, response)
    if status.is_server_error(code=response.status_code):
        raise ServerError("operation=server_error," + error_suffix, response)


def handle_request_error(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
        except (httpx.TimeoutException,) as exc:
            logger.exception(exc)
            raise ClientConnectionError() from exc

        validate_response(response)

        return response

    return wrapper


def handle_async_request_error(f):
    async def wrapper(*args, **kwargs):
        try:
            response = await f(*args, **kwargs)
        except (httpx.TimeoutException,) as exc:
            logger.exception(exc)
            raise ClientConnectionError() from exc

        validate_response(response)

        return response

    return wrapper
