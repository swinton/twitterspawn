#!/usr/bin/env python

import sys

import requests

from gevent import Greenlet

from oauth_hook import OAuthHook

from throttle import throttle_hook as throttle
from tasks import add_task, get_task, empty

class Worker(Greenlet):

    def __init__(self, access_token=None, access_token_secret=None, consumer_key=None, consumer_secret=None, header_auth=True, max_retries=5):
        Greenlet.__init__(self)

        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.header_auth = header_auth
        self.max_retries = max_retries

        oauth_hook = OAuthHook(access_token=access_token, access_token_secret=access_token_secret, 
                               consumer_key=consumer_key, consumer_secret=consumer_secret, 
                               header_auth=header_auth)
        
        self.hooks = dict(hooks={'pre_request': oauth_hook})

    def _run(self):
        while not empty():
            url, kwargs, callback, retries = get_task()
            
            # Default request method to GET
            kwargs.setdefault("method", "GET")

            # Include our OAuth hook
            kwargs.update(self.hooks)

            try:
                # Construct and send request
                request = requests.Request(url, **kwargs)
                request.send()
                response = request.response

            except requests.RequestException as e:
                sys.stderr.write("Error requesting %s: %s, " % (request.full_url, e.message))

                if retries < self.max_retries:
                    # Retry...
                    sys.stderr.write("retrying...\n")
                    add_task(url, kwargs, callback, retries + 1)

                else:
                    # Give up
                    sys.stderr.write("giving up...\n")

            else:
                # Invoke callback
                if callable(callback):
                    callback(response, self)

                # Stay within rate limits
                throttle(response)

        sys.stderr.write("%s exiting...\n" % str(self))

    def __str__(self):
        return 'Worker(%s, %s, %s, %s, %s)' % (self.access_token, self.access_token_secret, self.consumer_key, self.consumer_secret, self.header_auth)
