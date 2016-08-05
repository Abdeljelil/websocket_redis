import asyncio
import datetime

from websocket_redis.api.async import APIClientListener


class MyAPIClientListener(APIClientListener):

    @asyncio.coroutine
    def on_message(self, message):

        print(" in new on message function")
        new_massage = "async hi, {} , {}".format(
            message.client_id,
            datetime.datetime.now()
        )
        yield from message.reply(new_massage)

if __name__ == "__main__":

    redis_connection = dict(
        address=("localhost", 6379)
    )
    handler = MyAPIClientListener(redis_connection, app_name="test_app")
    loop = asyncio.get_event_loop()

    loop.run_until_complete(handler.run())
