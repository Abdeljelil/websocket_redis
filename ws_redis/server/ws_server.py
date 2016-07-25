import asyncio
import websockets
from websockets.exceptions import ConnectionClosed
from ws_redis.common.redis_manager import RedisManager
from ws_redis.server.ws_handler import WSHandler
import os

os.environ['PYTHONASYNCIODEBUG'] = '1'


class WSServer(object):

    def __init__(self, redis_manager):

        self.redis_manager = redis_manager

    @asyncio.coroutine
    def init(self):
        """
        """
        yield from self.redis_manager.init()

    @asyncio.coroutine
    def ws_handler_engine(self, websocket, path):
        """
            handler of all new Websockets
        """

        client = path.split("/")[-1]
        ws_handler = WSHandler(websocket, client, self.redis_manager)
        yield from ws_handler.init()
        try:
            producer_task = None
            listener_task = None
            while True:

                if listener_task is None or listener_task.get_stack() == []:
                    listener_task = asyncio.async(websocket.recv())

                if producer_task is None or producer_task.get_stack() == []:
                    producer_task = asyncio.async(ws_handler.send())

                done, pending = yield from asyncio.wait(
                    [listener_task, producer_task],
                    return_when=asyncio.FIRST_COMPLETED)

                if listener_task in done:
                    try:
                        message = listener_task.result()
                        yield from ws_handler.on_message(message)
                    except ConnectionClosed as e:
                        yield from ws_handler.on_error(e)
                        yield from ws_handler.on_close(e.code)
                        producer_task.cancel()
                        break

                if producer_task in done:
                    message = producer_task.result()
                    yield from websocket.send(message)

        except Exception as e:
            yield from ws_handler.on_error(e)
            yield from ws_handler.on_close(1001)

    @classmethod
    @asyncio.coroutine
    def run_server(cls, ws_connection, redis_connection):

        redis_manager = RedisManager(**redis_connection)

        yield from redis_manager.init()

        ws_handler = cls(redis_manager)

        print("Strting ws server {}".format(ws_connection))
        yield from websockets.serve(
            ws_handler.ws_handler_engine, **ws_connection)
