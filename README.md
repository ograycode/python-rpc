# Python RPC

## About

Python RPC is a backend agnostic rpc implementation, and simply a proof of concept at this stage. The goals of it is to have a very simple interface, and setup (dependingon the backend).

The only backend implemented is with `rq`, a redis queue implementation.

## Usage

### Setup

#### Server

1. Create a settings.py file with the following:
  1. `RPC_JOB_MAPPING` as a dict with the the key being a string and the value a function.
  2. `RPC_RECEIVER_BACKEND` is an instance of one of the available backends (`PythonRqBackend` is the only implementation).

#### Client

1. Create a settings.py file with the following:
  1. `RPC_CLIENT_BACKEND` is generally the same as `RPC_RECEIVER_BACKEND` on the server.

### Usage

Usage below is for demonstrative purposes only. A full working example can be found in the `example` folder.

#### Server

```python
from rpc import RpcReceiver

RpcReceiver().start()

def add(request):
    data = request.data
    answer = data['a'] + data['b']
    request.respond({'answer': answer})
```

#### Client

```python

from rpc import RpcClient

rpc_client = RpcClient()
rpc_client.call('add', data={'a': 3, 'b': 4})

response = rpc_client.call_and_wait(
    'add', data={'a': 1, 'b': 1}
)
assert response.data == 2
```

## API

`rpc.RpcClient` provides two methods:

  - `call` which takes a string `name` whose key matches to one of the functions in `RPC_JOB_MAPPING` on the server, and `data` which is a dictionary of values to be passed to the function on the server. This is a "fire and forget" operation.
  - `call_and_wait` that takes the same arguements as `call`, but returns a `Response` object.

`Response` is a class with the following attributes:

  - `data` is a dictionary of the return value.
  - `response_key` is the key used to fetch the response data.
  - `id` is a unique identifier matching the `Request` the server received

`Request` is a class passed into the receiving method on the server and has these attribtues:

  - `data` is the data passed from the client
  - `respond` method taking a dictonary to respond to the client with.
  - all other attributes are the same as `Response`

## Example

See the `example` folder for a working example. You can run the example by doing `docker-compose up`. If you receive a message that the worker is already registered, execute `docker-compose rm redis` and try again.

You will see logs from the client, worker and redis, with the `rpc` specific logs starting with `----->`.
