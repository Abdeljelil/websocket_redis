import asyncio
import logging
import unittest

import websockets

from websocket_redis.api.async import APIClientListener
from websocket_redis.common import asyncio_ensure_future
from websocket_redis.server import WSHandler, WSServer

# Avoid displaying stack traces at the ERROR logging level.
logging.basicConfig(level=logging.CRITICAL)

APP_NAME = 'test_app'
WS_PORT = 5678

REDIS_CONNECTION = dict(
    address=("localhost", 6379)
)


class MyAPIClientListener(APIClientListener):

    @asyncio.coroutine
    def on_message(self, message):

        yield from message.reply(message.text)


class MyWSHandler(WSHandler):

    @asyncio.coroutine
    def on_close(self, code):

        print("+++ Session ({}) has been closed, client : {}".format(
            self.session_id, self.client))

    @asyncio.coroutine
    def on_error(self, e):

        print("+++ Exception ({}) has been raised, client : {}".format(
            e, self.client))

    @asyncio.coroutine
    def on_message(self, text):

        print("+++ Receice message ({}) has been received for client : {}".format(
            text, self.client))

    @asyncio.coroutine
    def on_send(self, text):

        print("+++ Send message ({}) will be send to {}".format(
            text, self.client))


class ServerTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def run_loop_once(self):
        # Process callbacks scheduled with call_soon by appending a callback
        # to stop the event loop then running it until it hits that callback.
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()

    def start_server(self):

        ws_connection = dict(
            host="127.0.0.1",
            port=WS_PORT)

        self.server = WSServer(
            ws_connection=ws_connection,
            redis_connection=REDIS_CONNECTION,
            app_name=APP_NAME,
            ws_handler_class=MyWSHandler
        )

        self.loop.run_until_complete(self.server.run())

    def start_client(self, client):

        cor_connect = websockets.connect(
            'ws://127.0.0.1:{}/ws/{}'.format(WS_PORT, client))

        self.client_futrue = asyncio_ensure_future(cor_connect)
        new_client = self.loop.run_until_complete(self.client_futrue)

        return new_client

    def start_api(self):

        handler = MyAPIClientListener(
            REDIS_CONNECTION,
            app_name=APP_NAME)

        self.api_future = asyncio_ensure_future(handler.run())
        self.loop.call_soon_threadsafe(self.api_future)

    def test_01_send_one_client_async_api(self):

        message = "Hello!"

        self.start_api()

        self.start_server()
        client01 = self.start_client("client01")

        send_future = asyncio_ensure_future(client01.send(message))
        self.loop.run_until_complete(send_future)

        reply = self.loop.run_until_complete(client01.recv())

        self.assertEqual(message, reply)

        self.server.close()

        if not self.client_futrue.cancelled():
            self.client_futrue.cancel()

        if not self.api_future.cancelled():
            self.api_future.cancel()
