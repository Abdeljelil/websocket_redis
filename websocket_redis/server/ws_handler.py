import abc
import asyncio
import datetime
import json
import logging
from uuid import uuid1

import aioredis

logger = logging.getLogger(__name__)


class WSHandler(object):

    def __init__(self, client_id, redis_manager, app_name):
        """
        Args:
            client_id: str, client id who opened the websocket session.
            redis_manager: RedisManagerAIO instance to manage aioredis
                        connections.
            app_name : str, application name should be unique,
                    because you can connect many websocket_redis services
                    and app_name make the difference.

        Members:
            client : str, client id
            session_id : str and uuid format,
                    identify to the session opened for the client_id.
            redis: Redis-connection
            redis_manager: RedisManagerAIO instance
            app_name: service name useful in channel name for push/sub redis
            channel: client channel in push/sub redis
            redis_sub: push/sub redis connection
        """

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
        subscribe to Redis channel for the connected client

        this method is coroutine
        """

        self.redis_sub = yield from self.redis_manager.get_sub_connection()

        channel_name = "{}:{}".format(self.app_name, self.client)
        channels = yield from self.redis_sub.subscribe(channel_name)
        self.channel = channels[0]
        if isinstance(self.channel, aioredis.Channel) is False:
            logger.error(
                "Unalbe to join Redis channel {}".format(channel_name))

    @asyncio.coroutine
    def close(self, code):
        """
        this event runs when the client finish the session or
        an exception has been raised.
        this method is coroutine
        """

        yield from self.on_close(code)

        logger.info("Connection closed with code :{}".format(code))
        self.redis_sub.connection.close()
        channel_name = "{}:{}".format(self.app_name, self.client)
        logger.info("Unsubscribed from {} channel".format(channel_name))

    @abc.abstractmethod
    @asyncio.coroutine
    def on_close(self, code):
        """
        Override this method if you want to handle
        on_close event.
        Args :
            code : websocket code error.

        this method is coroutine
        """
        pass

    @abc.abstractmethod
    @asyncio.coroutine
    def on_error(self, e):
        """
        Override this method if you want to handle
        on_error event.
        Args:
            e: exception object
        this method is coroutine
        """
        pass

    @abc.abstractmethod
    @asyncio.coroutine
    def on_message(self, text):
        """
        Override this method if you want to handle the receive of message
        before the publish.
        Args:
            text : str, message has been sent
                    form the client to web-socket server
        this method is coroutine                
        """
        pass

    @abc.abstractmethod
    @asyncio.coroutine
    def on_send(self, text):
        """
        Override this method if you want to add
        extra work before the send of messages to client

        Args:
            text : str, message to send to client

        this method is coroutine
        """
        pass

    @asyncio.coroutine
    def publish(self, text):
        """
        listing message from the client and push the message to Redis
        to broadcast it to the API
        """

        yield from self.on_message(text)

        logger.info("Message received from {}, content: {}".format(
            self.client, text))

        msg_to_api = dict(client_id=self.client,
                          session_id=self.session_id,
                          text=text,
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
            message = decoded_msg["text"]

            yield from self.on_send(message)

            logger.info("{} message in {}: {}".format(
                self.session_id, self.channel.name, message))
            return message
