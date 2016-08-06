import asyncio
import logging
import unittest

import websockets

from websocket_redis.api.async import APIClientListener as BaseAsyncAPIListener
from websocket_redis.api.threading import \
    APIClientListener as BaseThreadAPIListener
from websocket_redis.common import asyncio_ensure_future
from websocket_redis.server import WSHandler, WSServer

# Avoid displaying stack traces at the ERROR logging level.
logging.basicConfig(level=logging.CRITICAL)

APP_NAME = 'test_app'
WS_PORT = 5678

REDIS_CONNECTION = dict(
    address=("localhost", 6379)
)


class ThreadAPIListener(BaseThreadAPIListener):

    def on_message(self, message):

        if message.client_id == "client01":
            message.reply("pong-thread!")
        else:
            message.reply("faild")


class AsyncAPIListener(BaseAsyncAPIListener):

    @asyncio.coroutine
    def on_message(self, message):

        # message.text
        if message.client_id == "client01":
            yield from message.reply("pong!")
        else:
            yield from message.reply("faild")


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

    def start_async_api(self):

        handler = AsyncAPIListener(
            REDIS_CONNECTION,
            app_name=APP_NAME)

        self.api_future = asyncio_ensure_future(handler.run())
        self.loop.call_soon_threadsafe(self.api_future)

    def start_threaded_api(self):

        redis_connection = dict(
            host=REDIS_CONNECTION["address"][0],
            port=REDIS_CONNECTION["address"][1],
        )
        self.thread_api = ThreadAPIListener(
            redis_connection,
            app_name=APP_NAME)

        self.loop.run_in_executor(None, self.thread_api.run)

    def test_01_send_one_client_async_api(self):

        message = "ping!"

        # start asynchronous api
        self.start_async_api()

        # start websocker server
        self.start_server()

        # start client simulator
        client01 = self.start_client("client01")

        # simulate send message from client
        send_future = asyncio_ensure_future(client01.send(message))
        self.loop.run_until_complete(send_future)

        # wait response from the api
        reply = self.loop.run_until_complete(client01.recv())

        # the reply should be pong from the api
        self.assertEqual("pong!", reply)

        # close all connections
        self.server.close()

        if not self.client_futrue.cancelled():
            self.client_futrue.cancel()

        if not self.api_future.cancelled():

            self.api_future.cancel()

    def test_02_send_one_client_threaded_api(self):

        print("-" * 20, " test02 ", "-" * 20)
        message = "ping!"

        self.start_threaded_api()

        self.start_server()
        client01 = self.start_client("client01")

        send_future = asyncio_ensure_future(client01.send(message))
        self.loop.run_until_complete(send_future)

        reply = self.loop.run_until_complete(client01.recv())
        print("*" * 30, reply)
        self.assertEqual("pong-thread!", reply)

        self.server.close()

        if not self.client_futrue.cancelled():
            self.client_futrue.cancel()

        self.thread_api.close()
