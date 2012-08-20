#!/usr/bin/env python

import requests

from gevent import Greenlet

from oauth_hook import OAuthHook

from throttle import throttle_hook as throttle
from tasks import add_task, get_task, empty

class Worker(Greenlet):

    def __init__(self, access_token=None, access_token_secret=None, consumer_key=None, consumer_secret=None, header_auth=None):
        Greenlet.__init__(self)

        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.header_auth = header_auth

        oauth_hook = OAuthHook(access_token=access_token, access_token_secret=access_token_secret, 
                               consumer_key=consumer_key, consumer_secret=consumer_secret, 
                               header_auth=header_auth)

        self.client = requests.session(hooks={'pre_request': oauth_hook})

    def _run(self):
        while not empty():
            url, kwargs, callback = get_task()

            response = self.client.get(url, **kwargs)
            
            if callable(callback):
                callback(response)

            throttle(response)

    def __str__(self):
        return 'Worker(%s, %s, %s, %s, %s)' % (self.access_token, self.access_token_secret, self.consumer_key, self.consumer_secret, self.header_auth)
