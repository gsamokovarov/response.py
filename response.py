'''
 _ __ ___  ___ _ __   ___  _ __  ___  ___   _ __  _   _
| '__/ _ \/ __| '_ \ / _ \| '_ \/ __|/ _ \ | '_ \| | | |
| | |  __/\__ \ |_) | (_) | | | \__ \  __/_| |_) | |_| |
|_|  \___||___/ .__/ \___/|_| |_|___/\___(_) .__/ \__, |
              |_|                          |_|    |___/
'''

from contextlib import contextmanager
from threading import local

# We _really_ want _everything_ from `requests`.
from requests import *


__title__     = 'response'
__author__    = 'Genadi Samokovarov'
__copyright__ = 'Copyrignt 2012 Genadi Samokovarov'


class ResponseStack(local):
    '''
    Thread-local stack of responses.
    '''

    def __init__(self):
        self.content = []

    def top(self):
        if self:
            return self.content[-1]

    def push(self, response):
        self.content.append(response)

    def pop(self):
        if self:
            try:
                return self.top()
            finally:
                del self.content[-1]

    __iter__    = lambda self: iter(self.content)
    __len__     = lambda self: len(self.content)
    __nonzero__ = lambda self: bool(self.content)
    __bool__    = __nonzero__


class ResponseProxy(local):
    '''
    Thread-local response objects proxy.
    '''

    def __init__(self, response_factory):
        self.response_factory = response_factory

    @property
    def response(self):
        return self.response_factory()

    @property
    def __class__(self):
        return self.response.__class__

    @property
    def __dict__(self):
        return self.response.__dict__

    __getattr__ = lambda self, name: getattr(self.response, name)
    __repr__    = lambda self: repr(self.response)
    __nonzero__ = lambda self: bool(self.response)
    __bool__    = __nonzero__


def convert_to_context_manager(func):
    '''
    Converts a `requests` API function to a context manager.
    '''

    def wrapper(*args, **kw):
        response = func(*args, **kw)

        try:
            yield responses.push(response)
        finally:
            responses.pop()

    return contextmanager(wrapper)


get     = convert_to_context_manager(get)
options = convert_to_context_manager(options)
head    = convert_to_context_manager(head)
post    = convert_to_context_manager(post)
put     = convert_to_context_manager(put)
patch   = convert_to_context_manager(patch)
delete  = convert_to_context_manager(delete)

request = convert_to_context_manager(request)

responses = ResponseStack()
response  = ResponseProxy(responses.top)
last      = response
