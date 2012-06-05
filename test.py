import inspect
import os

from attest import Tests, assert_hook, raises

from response import get, post, request, response


if 'HTTPBIN_URL' not in os.environ:
    os.environ['HTTPBIN_URL'] = 'http://httpbin.org/'

HTTPBIN_URL = os.environ.get('HTTPBIN_URL')


def httpbin(*suffix):
    """Returns url for HTTPBIN resource."""
    return HTTPBIN_URL + '/'.join(suffix)


suite = Tests()


@suite.test
def response_proxies_property_descriptors():
    with get(httpbin('get')):
        assert response.ok == True
        assert response.json['url'] == httpbin('get')


@suite.test
def nested_context_managers():
    with get(httpbin('get')):
        assert response.request.method == 'GET'

        with post(httpbin('post')):
            assert response.request.method == 'POST'

        assert response.request.method == 'GET'


@suite.test
def response_is_falsy_outside_context_managers():
    if response:
        raise AssertionError


if __name__ == "__main__":
    suite.run()
