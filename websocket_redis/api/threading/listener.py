import json
import logging
import time
from threading import Thread

from websocket_redis.api import AbstractListener
from websocket_redis.api.threading.message import Message
from websocket_redis.common.redis_manager import RedisManager

logger = logging.getLogger(__name__)


class APIClientListener(AbstractListener):

    def __init__(self, redis_connection, app_name):
        self.redis_connection = redis_connection
        self.app_name = app_name
        self.redis = None

    def run(self,):

        redis_manager = RedisManager(**self.redis_connection)
        redis_manager.init()
        self.redis = redis_manager.redis_global_connection

        redis_sub = redis_manager.get_sub_connection()
        redis_sub.subscribe(self.app_name)

        while True:
            message = redis_sub.get_message()
            if message:
                if message["type"] == 'message':
                    self._run_in_thead(message["data"])
            else:
                time.sleep(0.001)

    def _run_in_thead(self, raw_msg):

        str_msg = raw_msg.decode("utf-8")

        decoded_msg = json.loads(str_msg)

        message = Message(self, **decoded_msg)

        thread = Thread(target=self.on_message, args=(message, ))
        thread.start()

    def send(self, client_id, message):
        logger.info("send message {} to {}".format(client_id, message))
        channel_name = "{}:{}".format(self.app_name, client_id)
        self.redis.publish(channel_name, message)
