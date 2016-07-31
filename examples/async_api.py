import asyncio
from websocket_redis.api_async import APIClientListner


class MyWSHandler(APIClientListner):

    @asyncio.coroutine
    def on_message(self, message):

        print(" in new on message function")
        new_massage = "hi, {}".format(message.client_id)

        yield from message.reply(new_massage)

if __name__ == "__main__":

    redis_connection = dict(
        address=("localhost", 6379)
    )
    handler = MyWSHandler()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handler.run_listner(
        redis_connection, app_name="my_app"))
    loop.close()
