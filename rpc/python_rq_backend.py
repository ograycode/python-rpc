import json
import importlib
import os
import uuid
import logging
from rq import Queue, Connection
from rq.worker import HerokuWorker as Worker
from .rpc_settings import get_settings


listen = ['high', 'default', 'low']

def log(msg):
    # Verbose logging for this proof of concept
    print('-----> {msg}'.format(msg=msg))


def dispatch(name, data):
    from .rpc import _Request
    request = _Request(data)
    return get_settings().RPC_JOB_MAPPING[name](request)


class PythonRqBackend:

    def __init__(self, redis_client):
        self._redis_client = redis_client

    def start(self):
        log('Starting worker')
        with Connection(self._redis_client):
            worker = Worker(map(Queue, listen))
            worker.work()

    def call(self, name, data):
        log('Calling with the following: name={name} data={data}'.format(name=name, data=data))
        q = Queue(connection=self._redis_client)
        q.enqueue(dispatch, name, data)

    def call_and_wait(self, name, data):
        log('Calling and waiting for a response with the following: name={name} data={data}'.format(name=name, data=data))
        q = Queue(connection=self._redis_client)
        q.enqueue(dispatch, name, data)
        _, response = self._redis_client.blpop(data['response_key'])
        return json.loads(response)

    def respond(self, response_key, data):
        if response_key:
            log('Responding with response_key={response_key} data={data}'.format(response_key=response_key, data=data))
            self._redis_client.lpush(response_key, json.dumps(data))
            return True
        else:
            log('No response key found, not responding')
        return False
