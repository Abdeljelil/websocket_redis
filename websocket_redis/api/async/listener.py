import asyncio
import json
import logging

import aioredis

from websocket_redis.api import AbstractListener
from websocket_redis.api.async.message import Message
from websocket_redis.common.aioredis import RedisManagerAIO

logger = logging.getLogger(__name__)


class APIClientListener(AbstractListener):

    def __init__(self, redis_connection, app_name):
        self.redis_connection = redis_connection
        self.redis = None
        self.app_name = app_name

    @asyncio.coroutine
    def run(self):
        """
        connect to redis and keep listing on api-channel
        """

        redis_manager = RedisManagerAIO(**self.redis_connection)

        yield from redis_manager.init()
        self.redis = redis_manager.redis_global_connection
        redis_sub = yield from redis_manager.get_sub_connection()

        channels = yield from redis_sub.subscribe(self.app_name)
        channel = channels[0]
        if isinstance(channel, aioredis.Channel) is False:
            logger.error("Unable to join Redis channel")

        while (yield from channel.wait_message()):

            msg = yield from channel.get(encoding='utf-8')
            logger.info("new message {}".format(msg))
            decoded_msg = json.loads(msg)
            message = Message(self, **decoded_msg)
            yield from self.on_message(message)

    @asyncio.coroutine
    def send(self, client_id, message):
        logger.info("send message {} to {}".format(client_id, message))

        channel_name = "{}:{}".format(self.app_name, client_id)
        yield from self.redis.publish(channel_name, message)
