import asyncio
from ws_redis.api_threading import APIClientListner
import datetime


class MyWSHandler(APIClientListner):

    def on_message(self, message):

        print("in new on message function")
        new_massage = "hi, {} , {}".format(
            message.client_id,
            datetime.datetime.now()
            )

        message.reply(new_massage)

if __name__ == "__main__":

    redis_connection = dict(
        host="178.18.31.65",
        port=6666
    )
    handler = MyWSHandler()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handler.run_listner(redis_connection))
    loop.close()
