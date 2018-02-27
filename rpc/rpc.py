import uuid
import ujson as json
from .rpc_settings import get_settings



def _format_data_structure(users_data, response_key=None):
    return {
        'data': users_data,
        'id': str(uuid.uuid4()),
        'response_key': response_key
    }


class RpcClient:
    def __init__(self):
        self._backend = get_settings().RPC_CLIENT_BACKEND

    def call(self, name, data={}):
        data = _format_data_structure(data)
        self._backend.call(name, data)

    def call_and_wait(self, name, data={}):
        data = _format_data_structure(data, response_key=str(uuid.uuid4()))
        response = self._backend.call_and_wait(name, data)
        return _Response(response)


class RpcReceiver:
    def __init__(self):
        self._backend = get_settings().RPC_RECEIVER_BACKEND

    def start(self):
        self._backend.start()


class _Request:
    def __init__(self, request):
        for key, value in request.items():
            setattr(self, key, value)
        self._backend = get_settings().RPC_RECEIVER_BACKEND

    def respond(self, data):
        data = _format_data_structure(data, response_key=self.response_key)
        return self._backend.respond(self.response_key, data)


class _Response:
    def __init__(self, response):
        for key, value in response.items():
            setattr(self, key, value)
