import logging

import async_timeout
from json_encoder import json

from .decorators import handle_request_error, handle_async_request_error
from .models import Response

logger = logging.getLogger(__name__)


@handle_request_error
def make_request(session, request):
    logger.debug('operation=request_started, request={!r}'.format(request))
    method = request.method
    session_method = getattr(session, method.lower())
    client_response = session_method(
        request.url,
        params=request.params,
        data=request.body,
        headers=request.headers,
        timeout=request.timeout
    )
    content_type = client_response.headers.get('Content-Type', '')
    if 'text' in content_type:
        body = client_response.text
    elif 'json' in content_type:
        body = json.loads(client_response.text)
    else:
        body = client_response.content

    response = Response(
        url=client_response.url,
        method=method,
        body=body,
        headers=client_response.headers,
        status_code=client_response.status_code
    )
    logger.debug(
        'operation=request_finished, request={!r}, response={!r}'.format(
            request, response
        )
    )
    return response


@handle_async_request_error
async def make_async_request(session, request):
    logger.info('operation=request_started, request={!r}'.format(request))
    method = request.method
    with async_timeout.timeout(request.timeout):
        session_method = getattr(session, method.lower())
        async with session_method(request.url, params=request.params, data=request.body, headers=request.headers) as client_response:
            content_type = client_response.headers.get('Content-Type', '')
            if 'text' in content_type:
                body = await client_response.text()
            elif 'json' in content_type:
                body = json.loads(await client_response.text())
            else:
                body = await client_response.read()

            response = Response(
                url=str(client_response.url),
                method=method,
                body=body,
                headers=dict(client_response.headers),
                status_code=client_response.status
            )
            logger.info(
                'operation=request_finished, request={!r}, response={!r}'.format(
                    request, response
                )
            )
            return response
