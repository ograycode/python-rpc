import os
import sys
lib_path = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(lib_path)

from rpc import RpcClient

rpc_client = RpcClient()
rpc_client.call('add', data={'a': 3, 'b': 4})

response = rpc_client.call_and_wait(
    'add', data={'a': 1, 'b': 1}
)
print(response.data)
