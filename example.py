#!/usr/bin/env python

import twitterspawn

from settings import oauths

def callback(response):
    print "Got", response

def example(*requests):
    # Add requests
    for url, kwargs in requests:
        twitterspawn.add_request(url, kwargs, callback)

    # Add workers
    for oauth in oauths:
        twitterspawn.add_worker(access_token=oauth["access_token"], 
                                access_token_secret=oauth["access_token_secret"], 
                                consumer_key=oauth["consumer_key"], 
                                consumer_secret=oauth["consumer_secret"], 
                                header_auth=oauth["header_auth"])

    # Go!
    twitterspawn.go()

if __name__ == "__main__":
    example(("https://api.twitter.com/1/users/show.json", dict(params=dict(screen_name="stevewinton"))),
            ("https://api.twitter.com/1/users/show.json", dict(params=dict(screen_name="twitter"))),
            ("https://api.twitter.com/1/users/show.json", dict(params=dict(screen_name="barackobama"))),
            ("https://api.twitter.com/1/users/show.json", dict(params=dict(screen_name="nedsatomictweet"))),
            ("https://api.twitter.com/1/users/show.json", dict(params=dict(screen_name="catbinlady"))),)
