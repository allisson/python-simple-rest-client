import logging
from urllib.parse import urljoin

import requests
from json_encoder import json

from simple_rest_client.models import Request, Response
from simple_rest_client.decorators import handle_request_error

logger = logging.getLogger(__name__)


class BaseResource:
    def __init__(self, api_root_url=None, resource_name=None, action_urls={},
                 params={}, headers={}, timeout=None, append_slash=False,
                 json_encode_body=False):
        self.api_root_url = api_root_url
        self.resource_name = resource_name
        self.params = params
        self.headers = headers
        self.action_urls = action_urls or self.get_default_action_urls()
        self.timeout = timeout or 3
        self.append_slash = append_slash
        self.json_encode_body = json_encode_body

    def get_default_action_urls(self):
        return {
            'list': self.resource_name,
            'create': self.resource_name,
            'retrieve': self.resource_name + '/{}',
            'update': self.resource_name + '/{}',
            'partial_update': self.resource_name + '/{}',
            'destroy': self.resource_name + '/{}'
        }

    def get_full_url(self, action, *parts):
        url = self.action_urls.get(action, '').format(*parts)
        if not url:
            raise ValueError('No url match for "{}"'.format(action))
        if self.append_slash and not url.endswith('/'):
            url += '/'
        return urljoin(self.api_root_url, url)

    def build_request_instance(self, *args, action_name=None, method=None,
                               params=None, body=None, headers=None,
                               timeout=None):
        url = self.get_full_url(action_name, *args)
        return Request(
            url=url, method=method, params=params, body=body, headers=headers,
            timeout=timeout
        )


class Resource(BaseResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()

    @handle_request_error
    def make_request(self, request):
        logger.debug('operation=request_started, request={!r}'.format(request))
        method = getattr(self.session, request.method.lower())
        request.params.update(self.params)
        request.headers.update(self.headers)
        client_response = method(
            request.url,
            params=request.params,
            data=request.body,
            headers=request.headers,
            timeout=request.timeout
        )
        body = client_response.text
        content_type = client_response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            body = json.loads(body)

        response = Response(
            url=client_response.url,
            method=client_response.request.method,
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

    def list(self, *args, params={}, headers={}):
        request = self.build_request_instance(
            *args, action_name='list', method='GET', params=params, body=None,
            headers=headers, timeout=self.timeout
        )
        return self.make_request(request)

    def create(self, *args, body=None, params={}, headers={}):
        request = self.build_request_instance(
            *args, action_name='create', method='POST', params=params,
            body=body, headers=headers, timeout=self.timeout
        )
        return self.make_request(request)

    def retrieve(self, *args, params={}, headers={}):
        request = self.build_request_instance(
            *args, action_name='retrieve', method='GET', params=params,
            body=None, headers=headers, timeout=self.timeout
        )
        return self.make_request(request)

    def update(self, *args, body=None, params={}, headers={}):
        request = self.build_request_instance(
            *args, action_name='update', method='PUT', params=params,
            body=body, headers=headers, timeout=self.timeout
        )
        return self.make_request(request)

    def partial_update(self, *args, body=None, params={}, headers={}):
        request = self.build_request_instance(
            *args, action_name='partial_update', method='PATCH', params=params,
            body=body, headers=headers, timeout=self.timeout
        )
        return self.make_request(request)

    def destroy(self, *args, params={}, headers={}):
        request = self.build_request_instance(
            *args, action_name='destroy', method='DELETE', params=params,
            body=None, headers=headers, timeout=self.timeout
        )
        return self.make_request(request)
