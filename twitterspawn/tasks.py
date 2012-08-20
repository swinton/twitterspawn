#!/usr/bin/env python

from gevent.queue import Queue

queue = Queue()

def add_task(task_defn):
    return queue.put_nowait(task_defn)

def get_task():
    return queue.get()

def empty():
    return queue.empty()