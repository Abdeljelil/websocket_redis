import aioredis
import asyncio
import json
import os
from ws_redis.common.redis_manager import RedisManager
from ws_redis.api_async.message import Message


os.environ['PYTHONASYNCIODEBUG'] = '1'


class WSAPIHandler():

    @asyncio.coroutine
    def run_listner(self, redis_connection):
        """
        connect to redis and keep listing on api-channel
        """

        redis_manager = RedisManager(**redis_connection)

        yield from redis_manager.init()
        self.redis = redis_manager.redis_global_connection
        redis_sub = yield from redis_manager.get_sub_connection()

        channels = yield from redis_sub.subscribe("api_channel")
        channel = channels[0]
        if isinstance(channel, aioredis.Channel) is False:
            print("Unable to join Redis channel")

        while (yield from channel.wait_message()):
            msg = yield from channel.get(encoding='utf-8')
            print("new message {}".format(msg))
            decoded_msg = json.loads(msg)
            message = Message(self, **decoded_msg)
            yield from self.on_message(message)

    @asyncio.coroutine
    def on_message(self, message):
        """
        overide this method for your user case
        """
        # do something
        print('in basic on message function')
        pass

    @asyncio.coroutine
    def send(self, client_id, message):
        print("send message {} to {}".format(client_id, message))
        yield from self.redis.publish(client_id, message)
