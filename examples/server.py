import asyncio
from websocket_redis.server import WSServer, WSHandler


class MyWSHandler(WSHandler):

    @asyncio.coroutine
    def on_close(self, code):

        print("Session {} has been closed, client : {}".format(
            self.session_id, self.client))

    @asyncio.coroutine
    def on_error(self, e):

        print("Exception {} has been raised, client : {}".format(
            e, self.client))

    @asyncio.coroutine
    def on_message(self, message):

        print("Receice message \'{}\' has been received for client : {}".format(
            message, self.client))

    @asyncio.coroutine
    def on_send(self, message):

        print("Send message \'{}\' will be send to {}".format(
            message, self.client))

if __name__ == "__main__":

    ws_connection = dict(
        host="127.0.0.1",
        port=5678)

    redis_connection = dict(
        address=("localhost", 6379)
    )

    loop = asyncio.get_event_loop()
    server = WSServer(
        ws_connection=ws_connection,
        redis_connection=redis_connection,
        app_name="test_app",
        ws_handler_class=MyWSHandler
    )

    loop.run_until_complete(server.run())

    loop.run_forever()
    loop.close()
