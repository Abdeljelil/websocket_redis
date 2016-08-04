import unittest
import asyncio
import logging
import websockets

from websocket_redis.server import WSServer, WSHandler
from websocket_redis.api.async import APIClientListener


APP_NAME = 'test_app'
WS_PORT = 5678

REDIS_CONNECTION = dict(
    address=("localhost", 6379)
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MyAPIClientListener(APIClientListener):

    @asyncio.coroutine
    def on_message(self, message):

        yield from message.reply(message)


class MyWSHandler(WSHandler):

    @asyncio.coroutine
    def on_close(self, code):

        logger.info("+++ Session {} has been closed, client : {}".format(
            self.session_id, self.client))

    @asyncio.coroutine
    def on_error(self, e):

        print("+++ Exception {} has been raised, client : {}".format(
            e, self.client))

    @asyncio.coroutine
    def on_message(self, message):

        print("+++ Receice message \'{}\' has been received for client : {}".format(
            message, self.client))

    @asyncio.coroutine
    def on_send(self, message):

        print("+++ Send message \'{}\' will be send to {}".format(
            message, self.client))


class ServerTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        # asyncio.set_event_loop(self.loop)

    def tearDown(self):
        if self.loop.is_closed() is False:
            # self.loop.close()
            print("event loop is running")

    def start_async_api(self):

        handler = MyAPIClientListener(
            REDIS_CONNECTION,
            app_name=APP_NAME)

        yield from handler.run()

    @asyncio.coroutine
    def start_server(self):

        ws_connection = dict(
            host="127.0.0.1",
            port=WS_PORT)

        server = WSServer(
            ws_connection=ws_connection,
            redis_connection=REDIS_CONNECTION,
            app_name=APP_NAME,
            ws_handler_class=MyWSHandler
        )

        yield from server.run()

    @asyncio.coroutine
    def start_client(self, client):

        result = yield from websockets.connect(
            'ws://127.0.0.1:{}/ws/{}'.format(WS_PORT, client))

        return result

    def test_01_send_one_client_async_api(self):

        logger.info("in test 01")

        message = "Hello!"
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.start_server())
        websocket = self.loop.run_until_complete(self.start_client("client01"))

        logger.info(type(websocket))
        if self.loop.is_closed() is False:
            websocket = self.loop.run_until_complete(websocket.send(message))
            logger.info("message has been sent to client")
        else:
            logger.info("+++++ event loop is closed !!!!")

        # tasks = asyncio.wait([
        #     self.start_server(),
        #     self.start_client("client01"),

        # ])

        # done, pendding = self.loop.run_until_complete(tasks)

        # reply = self.loop.run_until_complete(websocket.recv())
        # print(reply)
        # self.assertEqual(reply, "Hello!")
        # self.loop.run_forever()
