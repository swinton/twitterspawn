#!/usr/bin/env python

from gevent.queue import Queue

queue = Queue()

def add_task(url, kwargs, callback=None, retries=0):
    return queue.put_nowait(Task(url, kwargs, callback, retries))

def get_task():
    return queue.get()

def empty():
    return queue.empty()

class Task():
    """
    Encapsulates a task definition.
    """
    def __init__(self, url, kwargs, callback=None, retries=0):
        self.url = url
        self.kwargs = kwargs
        self.callback = callback
        self.retries = retries

    def __iter__(self):
        # For easy unpacking of task
        return iter((self.url, self.kwargs, self.callback, self.retries))
