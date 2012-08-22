#!/usr/bin/env python

import gevent

from tasks import add_task, get_task, empty
from worker import Worker

workers = []

def add_request(url, kwargs, callback=None):
    add_task(url, kwargs, callback)

def add_worker(access_token=None, access_token_secret=None, consumer_key=None, consumer_secret=None, header_auth=True):
    worker = Worker(access_token=access_token, access_token_secret=access_token_secret, consumer_key=consumer_key, consumer_secret=consumer_secret, header_auth=header_auth)
    workers.append(worker)

def go():
    for worker in workers:
        worker.start()
    gevent.joinall(workers)
