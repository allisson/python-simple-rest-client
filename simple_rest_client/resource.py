import logging
from urllib.parse import urljoin

import requests
from json_encoder import json

from simple_rest_client.models import Request, Response
from simple_rest_client.decorators import handle_request_error

logger = logging.getLogger(__name__)


class BaseResource:
    def __init__(self, api_root_url=None, resource_name=None, action_urls={},
                 headers={}, timeout=None, append_slash=False,
                 json_encode_body=False):
        self.api_root_url = api_root_url
        self.resource_name = resource_name
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


class Resource(BaseResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()

    @handle_request_error
    def make_request(self, request):
        method = getattr(self.session, request.method.lower())
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

        return Response(
            url=client_response.url,
            method=client_response.request.method,
            body=body,
            headers=client_response.headers,
            status_code=client_response.status_code
        )

    def list(self, *args, **kwargs):
        url = self.get_full_url('list', *args)
        request = Request(
            url=url, method='GET', params=kwargs, body=None,
            headers=self.headers, timeout=self.timeout
        )
        return self.make_request(request)

    def create(self, *args, body=None, **kwargs):
        url = self.get_full_url('create', *args)
        if self.json_encode_body:
            body = json.dumps(body)
        request = Request(
            url=url, method='POST', params=kwargs, body=body,
            headers=self.headers, timeout=self.timeout
        )
        return self.make_request(request)

    def retrieve(self, *args, **kwargs):
        url = self.get_full_url('retrieve', *args)
        request = Request(
            url=url, method='GET', params=kwargs, body=None,
            headers=self.headers, timeout=self.timeout
        )
        return self.make_request(request)

    def update(self, *args, body=None, **kwargs):
        url = self.get_full_url('update', *args)
        if self.json_encode_body and body:
            body = json.dumps(body)
        request = Request(
            url=url, method='PUT', params=kwargs, body=body,
            headers=self.headers, timeout=self.timeout
        )
        return self.make_request(request)

    def partial_update(self, *args, body=None, **kwargs):
        url = self.get_full_url('partial_update', *args)
        if self.json_encode_body and body:
            body = json.dumps(body)
        request = Request(
            url=url, method='PATCH', params=kwargs, body=body,
            headers=self.headers, timeout=self.timeout
        )
        return self.make_request(request)

    def destroy(self, *args, **kwargs):
        url = self.get_full_url('destroy', *args)
        request = Request(
            url=url, method='DELETE', params=kwargs, body=None,
            headers=self.headers, timeout=self.timeout
        )
        return self.make_request(request)
