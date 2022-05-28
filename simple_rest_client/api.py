from slugify import slugify

from simple_rest_client.resource import Resource


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

    def add_resource(
        self,
        api_root_url=None,
        resource_name=None,
        resource_class=None,
        params=None,
        headers=None,
        timeout=None,
        append_slash=None,
        json_encode_body=None,
        ssl_verify=None,
    ):
        resource_class = resource_class or Resource
        resource = resource_class(
            api_root_url=api_root_url if api_root_url is not None else self.api_root_url,
            resource_name=resource_name,
            params=params if params is not None else self.params,
            headers=headers if headers is not None else self.headers,
            timeout=timeout if timeout is not None else self.timeout,
            append_slash=append_slash if append_slash is not None else self.append_slash,
            json_encode_body=json_encode_body if json_encode_body is not None else self.json_encode_body,
            ssl_verify=ssl_verify if ssl_verify is not None else self.ssl_verify,
        )
        self._resources[resource_name] = resource
        resource_valid_name = self.correct_attribute_name(resource_name)
        setattr(self, resource_valid_name, resource)

    def get_resource_list(self):
        return list(self._resources.keys())

    def correct_attribute_name(self, name):
        slug_name = slugify(name)
        return slug_name.replace("-", "_")
