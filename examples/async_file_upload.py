import asyncio

from simple_rest_client.api import API
from simple_rest_client.resource import AsyncResource


class FileUploadResource(AsyncResource):
    actions = {
        'create': {'method': 'POST', 'url': 'post.php?dir=example'},
    }


# http://blog.henrycipolla.com/2011/12/testing-multipartform-data-uploads-with-post-test-server/
files = {'file': open('github.py', 'rb')}
post_test_server_api = API(api_root_url='http://posttestserver.com/', timeout=10)
post_test_server_api.add_resource(resource_name='file_upload', resource_class=FileUploadResource)


async def main():
    response = await post_test_server_api.file_upload.create(body=files)
    print('post_test_server_api.file_upload.create={!r}'.format(response.body))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
