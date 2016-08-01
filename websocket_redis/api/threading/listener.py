import json
import time
from threading import Thread

from websocket_redis.common.redis_manager import RedisManager
from websocket_redis.api.threading.message import Message
from websocket_redis.api import AbstractListener


class APIClientListener(AbstractListener):

    def __init__(self):
        self.app_name = None
        self.redis = None

    def run(self, redis_connection, app_name):

        self.app_name = app_name
        redis_manager = RedisManager(**redis_connection)
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
        print("send message {} to {}".format(client_id, message))
        channel_name = "{}:{}".format(self.app_name, client_id)
        self.redis.publish(channel_name, message)
