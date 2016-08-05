import asyncio
import logging

import websockets
from websockets.exceptions import ConnectionClosed
from websocket_redis.common.aioredis import RedisManagerAIO
from websocket_redis.server.ws_handler import WSHandler
from websocket_redis.common import asyncio_ensure_future

logger = logging.getLogger(__name__)


class WSServer(object):

    def __init__(self, ws_connection, redis_connection, app_name="myapp", ws_handler_class=WSHandler):

        self.ws_connection = ws_connection
        self.redis_connection = redis_connection
        self.app_name = app_name
        self.ws_handler_class = ws_handler_class
        self.redis_manager = None
        self.server = None

    def close(self):

        self.server.close()

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                asyncio.wait_for(self.server.wait_closed(), timeout=1))
        except asyncio.TimeoutError:
            logger.warning("Server failed to stop")

        self.redis_manager.close()

    @asyncio.coroutine
    def ws_handler_engine(self, websocket, path):
        """
            handler of all new Websockets
        """

        client = path.split("/")[-1]
        ws_handler = self.ws_handler_class(
            client_id=client,
            redis_manager=self.redis_manager,
            app_name=self.app_name
        )

        yield from ws_handler.init()

        producer_task = None
        listener_task = None
        while True:

            if listener_task is None or listener_task.get_stack() == []:
                listener_task = asyncio_ensure_future(websocket.recv())

            if producer_task is None or producer_task.get_stack() == []:
                producer_task = asyncio_ensure_future(ws_handler.send())

            done, _ = yield from asyncio.wait(
                [listener_task, producer_task],
                return_when=asyncio.FIRST_COMPLETED)

            if listener_task in done:
                try:
                    message = listener_task.result()
                    yield from ws_handler.publish(message)
                except ConnectionClosed as ecc:
                    yield from ws_handler.on_error(ecc)
                    yield from ws_handler.close(ecc.code)
                    producer_task.cancel()
                    break

            if producer_task in done:
                message = producer_task.result()
                yield from websocket.send(message)

    @asyncio.coroutine
    def run(self):

        self.redis_manager = RedisManagerAIO(**self.redis_connection)

        yield from self.redis_manager.init()

        logger.info("Strting ws server {}".format(self.ws_connection))

        self.server = yield from websockets.serve(
            self.ws_handler_engine, **self.ws_connection)

        return self.server
