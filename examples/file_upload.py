from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class FileUploadResource(Resource):
    actions = {
        'create': {'method': 'POST', 'url': 'post.php?dir=example'},
    }


# http://blog.henrycipolla.com/2011/12/testing-multipartform-data-uploads-with-post-test-server/
files = {'file': open('github.py', 'rb')}
post_test_server_api = API(api_root_url='http://posttestserver.com/', timeout=10)
post_test_server_api.add_resource(resource_name='file_upload', resource_class=FileUploadResource)
print('post_test_server_api.file_upload.create={!r}'.format(post_test_server_api.file_upload.create(files=files).body))
