import logging
from urllib.parse import urljoin
from types import MethodType

import requests
from json_encoder import json

from simple_rest_client.models import Request, Response
from simple_rest_client.decorators import handle_request_error
from simple_rest_client.exceptions import ActionNotFound, ActionURLMatchError

logger = logging.getLogger(__name__)


class BaseResource:
    actions = {}

    def __init__(self, api_root_url=None, resource_name=None, params={},
                 headers={}, timeout=None, append_slash=False,
                 json_encode_body=False):
        self.api_root_url = api_root_url
        self.resource_name = resource_name
        self.params = params
        self.headers = headers
        self.timeout = timeout or 3
        self.append_slash = append_slash
        self.json_encode_body = json_encode_body
        self.actions = self.actions or self.default_actions

        for action_name in self.actions.keys():
            self.add_action(action_name)

    @property
    def default_actions(self):
        return {
            'list': {
                'method': 'GET',
                'url': self.resource_name
            },
            'create': {
                'method': 'POST',
                'url': self.resource_name
            },
            'retrieve': {
                'method': 'GET',
                'url': self.resource_name + '/{}',
            },
            'update': {
                'method': 'PUT',
                'url': self.resource_name + '/{}',
            },
            'partial_update': {
                'method': 'PATCH',
                'url': self.resource_name + '/{}',
            },
            'destroy': {
                'method': 'DELETE',
                'url': self.resource_name + '/{}',
            },
        }

    def get_action(self, action_name):
        try:
            return self.actions[action_name]
        except KeyError:
            raise ActionNotFound('action "{}" not found'.format(action_name))

    def get_action_full_url(self, action_name, *parts):
        action = self.get_action(action_name)
        try:
            url = action['url'].format(*parts)
        except IndexError:
            raise ActionURLMatchError('No url match for "{}"'.format(action_name))

        if self.append_slash and not url.endswith('/'):
            url += '/'
        return urljoin(self.api_root_url, url)

    def get_action_method(self, action_name):
        action = self.get_action(action_name)
        return action['method']

    def add_action(self, action_name):
        def action_method(self, *args, body=None, params={}, headers={},
                          action_name=action_name):
            url = self.get_action_full_url(action_name, *args)
            method = self.get_action_method(action_name)
            if self.json_encode_body and body:
                body = json.dumps(body)
            request = Request(
                url=url, method=method, params=params, body=body,
                headers=headers, timeout=self.timeout
            )
            return self.make_request(request)

        setattr(self, action_name, MethodType(action_method, self))


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
