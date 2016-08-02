import os
import asyncio

import websockets
from websockets.exceptions import ConnectionClosed
from websocket_redis.common.aioredis import RedisManagerAIO
from websocket_redis.server.ws_handler import WSHandler

os.environ['PYTHONASYNCIODEBUG'] = '1'


class WSServer(object):

    def __init__(self, redis_manager, app_name):

        self.redis_manager = redis_manager
        self.app_name = app_name

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
        ws_handler = WSHandler(
            websocket, client, self.redis_manager, self.app_name)
        yield from ws_handler.init()

        producer_task = None
        listener_task = None
        while True:

            if listener_task is None or listener_task.get_stack() == []:
                listener_task = asyncio.async(websocket.recv())

            if producer_task is None or producer_task.get_stack() == []:
                producer_task = asyncio.async(ws_handler.send())

            done, _ = yield from asyncio.wait(
                [listener_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED)

            if listener_task in done:
                try:
                    message = listener_task.result()
                    yield from ws_handler.on_message(message)
                except ConnectionClosed as ecc:
                    yield from ws_handler.on_error(ecc)
                    yield from ws_handler.on_close(ecc.code)
                    producer_task.cancel()
                    break

            if producer_task in done:
                message = producer_task.result()
                yield from websocket.send(message)

    @classmethod
    @asyncio.coroutine
    def run_server(cls, ws_connection, redis_connection, app_name="myapp"):

        redis_manager = RedisManagerAIO(**redis_connection)

        yield from redis_manager.init()

        ws_handler = cls(redis_manager, app_name)

        print("Strting ws server {}".format(ws_connection))
        yield from websockets.serve(
            ws_handler.ws_handler_engine, **ws_connection)
