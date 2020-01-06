from slugify import slugify

from .resource import Resource


class API:
    def __init__(
        self,
        api_root_url=None,
        params=None,
        headers=None,
        timeout=None,
        append_slash=False,
        json_encode_body=False,
        ssl_verify=None,
    ):
        self.api_root_url = api_root_url
        self.params = params or {}
        self.headers = headers or {}
        self.timeout = timeout
        self.append_slash = append_slash
        self.json_encode_body = json_encode_body
        self.ssl_verify = True if ssl_verify is None else ssl_verify
        self._resources = {}

        if self.json_encode_body:
            self.headers["Content-Type"] = "application/json"

    def add_resource(
        self,
        api_root_url=None,
        resource_name=None,
        resource_class=None,
        params=None,
        headers=None,
        timeout=None,
        append_slash=False,
        json_encode_body=False,
    ):
        resource_valid_name = self.correct_attribute_name(resource_name)
        resource_class = resource_class or Resource
        resource = resource_class(
            api_root_url=api_root_url or self.api_root_url,
            resource_name=resource_valid_name,
            params=params or self.params,
            headers=headers or self.headers,
            timeout=timeout or self.timeout,
            append_slash=append_slash or self.append_slash,
            json_encode_body=json_encode_body or self.json_encode_body,
            ssl_verify=self.ssl_verify,
        )
        self._resources[resource_valid_name] = resource
        setattr(self, resource_valid_name, resource)

    def get_resource_list(self):
        return list(self._resources.keys())

    def correct_attribute_name(self, name):
        slug_name = slugify(name)
        return slug_name.replace("-", "_")
