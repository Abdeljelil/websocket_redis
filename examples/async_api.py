import asyncio
from ws_redis.api_async import WSAPIHandler


class MyWSHandler(WSAPIHandler):

    @asyncio.coroutine
    def on_message(self, message):

        print(" in new on message function")
        new_massage = "hi, {}".format(message.client_id)

        yield from message.reply(new_massage)

if __name__ == "__main__":

    redis_connection = dict(
        address=("178.18.31.65", 6666)
    )
    handler = MyWSHandler()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handler.run_listner(redis_connection))
    loop.close()
