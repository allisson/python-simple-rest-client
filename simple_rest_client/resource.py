import logging
from types import MethodType

import httpx

from .exceptions import ActionNotFound, ActionURLMatchError
from .models import Request
from .request import make_async_request, make_request

logger = logging.getLogger(__name__)


class BaseResource:
    actions = {}

    def __init__(
        self,
        api_root_url=None,
        resource_name=None,
        params=None,
        headers=None,
        timeout=None,
        append_slash=False,
        json_encode_body=False,
        ssl_verify=None,
    ):
        self.api_root_url = api_root_url
        self.resource_name = resource_name
        self.params = params or {}
        self.headers = headers or {}
        self.timeout = timeout or 3
        self.append_slash = append_slash
        self.json_encode_body = json_encode_body
        self.actions = self.actions or self.default_actions
        self.ssl_verify = True if ssl_verify is None else ssl_verify

        if self.json_encode_body:
            self.headers["Content-Type"] = "application/json"

    @property
    def default_actions(self):
        return {
            "list": {"method": "GET", "url": self.resource_name},
            "create": {"method": "POST", "url": self.resource_name},
            "retrieve": {"method": "GET", "url": self.resource_name + "/{}"},
            "update": {"method": "PUT", "url": self.resource_name + "/{}"},
            "partial_update": {"method": "PATCH", "url": self.resource_name + "/{}"},
            "destroy": {"method": "DELETE", "url": self.resource_name + "/{}"},
        }

    def get_action(self, action_name):
        try:
            return self.actions[action_name]
        except KeyError:
            raise ActionNotFound('action "{}" not found'.format(action_name))

    def get_action_full_url(self, action_name, *parts):
        action = self.get_action(action_name)
        try:
            url = action["url"].format(*parts)
        except IndexError:
            raise ActionURLMatchError('No url match for "{}"'.format(action_name))

        if self.append_slash and not url.endswith("/"):
            url += "/"
        if not self.api_root_url.endswith("/"):
            self.api_root_url += "/"
        if url.startswith("/"):
            url = url.replace("/", "", 1)
        return self.api_root_url + url

    def get_action_method(self, action_name):
        action = self.get_action(action_name)
        return action["method"]


class Resource(BaseResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = httpx.Client(verify=self.ssl_verify)
        for action_name in self.actions.keys():
            self.add_action(action_name)

    def add_action(self, action_name):
        def action_method(
            self, *args, body=None, params=None, headers=None, action_name=action_name, **kwargs
        ):
            url = self.get_action_full_url(action_name, *args)
            method = self.get_action_method(action_name)
            request = Request(
                url=url,
                method=method,
                params=params or {},
                body=body,
                headers=headers or {},
                timeout=self.timeout,
                kwargs=kwargs,
            )
            request.params.update(self.params)
            request.headers.update(self.headers)
            return make_request(self.client, request)

        setattr(self, action_name, MethodType(action_method, self))


class AsyncResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = httpx.AsyncClient(verify=self.ssl_verify)
        for action_name in self.actions.keys():
            self.add_action(action_name)

    def add_action(self, action_name):
        async def action_method(
            self, *args, body=None, params=None, headers=None, action_name=action_name, **kwargs
        ):
            url = self.get_action_full_url(action_name, *args)
            method = self.get_action_method(action_name)
            request = Request(
                url=url,
                method=method,
                params=params or {},
                body=body,
                headers=headers or {},
                timeout=self.timeout,
                kwargs=kwargs,
            )
            request.params.update(self.params)
            request.headers.update(self.headers)
            async with self.client as client:
                return await make_async_request(client, request)

        setattr(self, action_name, MethodType(action_method, self))
