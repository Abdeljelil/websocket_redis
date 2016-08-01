import asyncio
from websocket_redis.api.threading import APIClientListener
import datetime


class MyWSHandler(APIClientListener):

    def on_message(self, message):

        print("in new on message function")
        new_massage = "thread hi, {} , {}".format(
            message.client_id,
            datetime.datetime.now()
        )

        message.reply(new_massage)

if __name__ == "__main__":

    redis_connection = dict(
        host="localhost",
        port=6379
    )
    handler = MyWSHandler()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handler.run(
        redis_connection, app_name="my_app"))
    loop.close()
