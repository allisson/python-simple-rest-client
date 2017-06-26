import logging
from types import MethodType
from urllib.parse import urljoin

import aiohttp
import requests
from json_encoder import json

from .exceptions import ActionNotFound, ActionURLMatchError
from .models import Request
from .request import make_request, make_async_request

logger = logging.getLogger(__name__)


class BaseResource:
    actions = {}

    def __init__(self, api_root_url=None, resource_name=None, params=None,
                 headers=None, timeout=None, append_slash=False,
                 json_encode_body=False):
        self.api_root_url = api_root_url
        self.resource_name = resource_name
        self.params = params or {}
        self.headers = headers or {}
        self.timeout = timeout or 3
        self.append_slash = append_slash
        self.json_encode_body = json_encode_body
        self.actions = self.actions or self.default_actions

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


class Resource(BaseResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()
        for action_name in self.actions.keys():
            self.add_action(action_name)

    def add_action(self, action_name):
        def action_method(self, *args, body=None, params=None, headers=None,
                          action_name=action_name):
            url = self.get_action_full_url(action_name, *args)
            method = self.get_action_method(action_name)
            if self.json_encode_body and body:
                body = json.dumps(body)
            request = Request(
                url=url,
                method=method,
                params=params or {},
                body=body,
                headers=headers or {},
                timeout=self.timeout
            )
            request.params.update(self.params)
            request.headers.update(self.headers)
            return make_request(self.session, request)

        setattr(self, action_name, MethodType(action_method, self))


class AsyncResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for action_name in self.actions.keys():
            self.add_action(action_name)

    def add_action(self, action_name):
        async def action_method(self, *args, body=None, params=None,
                                headers=None, action_name=action_name):
            url = self.get_action_full_url(action_name, *args)
            method = self.get_action_method(action_name)
            if self.json_encode_body and body:
                body = json.dumps(body)
            request = Request(
                url=url,
                method=method,
                params=params or {},
                body=body,
                headers=headers or {},
                timeout=self.timeout
            )
            request.params.update(self.params)
            request.headers.update(self.headers)
            async with aiohttp.ClientSession() as session:
                return await make_async_request(session, request)

        setattr(self, action_name, MethodType(action_method, self))
