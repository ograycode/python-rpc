import os
import sys
lib_path = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(lib_path)

from rpc import RpcReceiver

RpcReceiver().start()
