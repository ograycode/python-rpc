from calc import add
from connection import redis_client
from rpc.python_rq_backend import PythonRqBackend

RPC_JOB_MAPPING = {'add': add}
RPC_CLIENT_BACKEND = PythonRqBackend(redis_client)
RPC_RECEIVER_BACKEND = RPC_CLIENT_BACKEND
