from ws_redis.common.redis_manager import RedisManager
from ws_redis.api_threading.message import Message

import json
import time
from threading import Thread


class APIClientListner(object):

    def run_listner(self, redis_connection):

        redis_manager = RedisManager(**redis_connection)
        redis_manager.init()
        self.redis = redis_manager.redis_global_connection

        redis_sub = redis_manager.get_sub_connection()
        redis_sub.subscribe("api_channel")

        while True:
            message = redis_sub.get_message()
            if message:
                if message["type"] == 'message':
                    self.run_in_thead(message["data"])
            else:
                time.sleep(0.001)

    def run_in_thead(self, raw_msg):

        str_msg = raw_msg.decode("utf-8")

        decoded_msg = json.loads(str_msg)

        message = Message(self, **decoded_msg)

        thread = Thread(target=self.on_message, args=(message, ))
        thread.start()
        print("new thread has been started")

    def on_message(self, message):
        """
        overide this method for your user case
        """
        # do something
        print('in basic on_message function')

        self.send("")

    def send(self, client_id, message):
        print("send message {} to {}".format(client_id, message))
        self.redis.publish(client_id, message)
