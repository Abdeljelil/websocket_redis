import aioredis
import asyncio
import json
import os
from websocket_redis.common.redis_manager import RedisManagerAIO
from websocket_redis.api_async.message import Message


os.environ['PYTHONASYNCIODEBUG'] = '1'


class APIClientListner(object):

    @asyncio.coroutine
    def run_listner(self, redis_connection, app_name):
        """
        connect to redis and keep listing on api-channel
        """
        self.app_name = app_name
        redis_manager = RedisManagerAIO(**redis_connection)

        yield from redis_manager.init()
        self.redis = redis_manager.redis_global_connection
        redis_sub = yield from redis_manager.get_sub_connection()

        channels = yield from redis_sub.subscribe(self.app_name)
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
        print('in basic on_message function')
        pass

    @asyncio.coroutine
    def send(self, client_id, message):
        print("send message {} to {}".format(client_id, message))
        channel_name = "{}:{}".format(self.app_name, client_id)
        yield from self.redis.publish(channel_name, message)
