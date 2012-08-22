#!/usr/bin/env python

import datetime
import sys

import gevent

def throttle_hook(response):
    ratelimited = "x-ratelimit-remaining" in response.headers and \
                  "x-ratelimit-reset" in response.headers 

    if ratelimited:
        remaining = int(response.headers["x-ratelimit-remaining"])
        reset = datetime.datetime.utcfromtimestamp(float(response.headers["x-ratelimit-reset"]))
        now = datetime.datetime.utcnow()
        
        time_to_reset = reset - now
        time_to_sleep = time_to_reset.total_seconds() / remaining if remaining > 0 else 0

        sys.stderr.write("%d requests remaining. Sleeping for %.2f secs...\n" % (remaining, time_to_sleep))
        gevent.sleep(time_to_sleep)
