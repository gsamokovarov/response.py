import inspect
import os

from attest import Tests, assert_hook, raises

from response import get, post, request, response, \
                     ResponseStack, ResponseProxy


if 'HTTPBIN_URL' not in os.environ:
    os.environ['HTTPBIN_URL'] = 'http://httpbin.org/'

HTTPBIN_URL = os.environ.get('HTTPBIN_URL')


def httpbin(*suffix):
    """Returns url for HTTPBIN resource."""
    return HTTPBIN_URL + '/'.join(suffix)


suite = Tests()


@apply
def response_stack_suite():
    stack = Tests()

    @stack.context
    def prepare_new_stack():
        yield ResponseStack()
        
    @stack.test
    def pop_returns_the_removed_item(stack):
        stack.push(1)

        assert stack.pop() == 1
        assert len(stack) == 0

    @stack.test
    def top_is_null_if_stack_is_empty(stack):
        assert stack.top() is None

    return stack


@apply
def response_proxy_suite():
    proxy = Tests()

    class Response(object):
        pass

    @proxy.context
    def prepare_new_proxy():
        yield ResponseProxy(Response)

    @proxy.test
    def is_instance_of_the_target(proxy):
        assert isinstance(proxy, Response) 

    return proxy


suite.register(response_stack_suite)
suite.register(response_proxy_suite)


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
