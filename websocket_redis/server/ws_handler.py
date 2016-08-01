import datetime
import json
from uuid import uuid1
import asyncio

import aioredis


class WSHandler():

    def __init__(self, websocket, client_id, redis_manager, app_name):
        """
        """
        self.websocket = websocket
        self.client = client_id
        self.session_id = str(uuid1())
        self.redis = redis_manager.redis_global_connection
        self.redis_manager = redis_manager
        self.app_name = app_name
        self.channel = None
        self.redis_sub = None

    @asyncio.coroutine
    def init(self):
        """
        setup the new session
        Create new subscription connection to Redis
        subscribe to Redis channel to the connected client
        """

        self.redis_sub = yield from self.redis_manager.get_sub_connection()

        channel_name = "{}:{}".format(self.app_name, self.client)
        channels = yield from self.redis_sub.subscribe(channel_name)
        self.channel = channels[0]
        if isinstance(self.channel, aioredis.Channel) is False:
            print("Unable to join Redis channel")

    @asyncio.coroutine
    def on_close(self, code):
        """
        this event runs when the client finish the session or
        an exception has been raised.
        """
        print("Connection closed with code :{}".format(code))
        self.redis_sub.connection.close()
        print("Unsubscribed from {} channel".format(self.channel))

    @asyncio.coroutine
    def on_error(self, e):
        """

        """
        print(type(e))
        print("Error {}".format(e), self.session_id)

    @asyncio.coroutine
    def on_message(self, message):
        """
        listing message from the client and push the message to Redis
        to broadcast it to the API
        """
        print("Message recieved from {}, content: {}".format(
            self.client, message))

        msg_to_api = dict(client_id=self.client,
                          session_id=self.session_id,
                          message=message,
                          create_on=str(datetime.datetime.now())
                          )

        yield from self.redis.publish(self.app_name, json.dumps(msg_to_api))

    @asyncio.coroutine
    def send(self):
        """
        listing on Redis channel and send message received on
        this channels to client
        """
        while (yield from self.channel.wait_message()):
            wrapped_msg = yield from self.channel.get(encoding='utf-8')
            decoded_msg = json.loads(wrapped_msg)
            message = decoded_msg["message"]
            print("{} message in {}: {}".format(
                self.session_id, self.channel.name, message))
            return message
        return None
