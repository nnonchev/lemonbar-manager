from contextlib import contextmanager

import zmq
import zmq.asyncio


@contextmanager
def get_async_server_sock():
    """ Yields socket (via context manager) for a server using ZeroMQ """

    try:
        ctx = zmq.asyncio.Context()
        sock = ctx.socket(zmq.REP)
        sock.bind("tcp://*:5555")

        yield sock
    except Exception as err:
        print(f"Unexcepted ZMQ error: { err }")
    finally:
        ctx.destroy()
