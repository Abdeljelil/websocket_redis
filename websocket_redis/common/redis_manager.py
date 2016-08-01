import asyncio

import redis
import aioredis


class RedisManager(object):

    def __init__(self, host='localhost', port=6379,
                 db=0, password=None, **kwargs):
        """
        initiate Redis connection parameters
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.conn_kw = kwargs
        self.redis_global_connection = None

    def _get_connection(self):
        """
        create new Redis connection
        for more details see create_redis function in redis module
        """
        connection = redis.StrictRedis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            **self.conn_kw
        )
        return connection

    def init(self):
        """
        create new Redis global connection
        """
        print("create new Redis instance")
        self.redis_global_connection = self._get_connection()

    def get_sub_connection(self):
        """
        create new connection as subscribe connection to Redis server
        """
        sub_connection = self._get_connection().pubsub()

        return sub_connection


class RedisManagerAIO(object):

    def __init__(self, address, *,
                 db=0, password=None, ssl=None, encoding=None, loop=None):
        """
        initiate Redis connection parameters
        """
        self.address = address
        self.db = db
        self.password = password
        self.ssl = ssl
        self.encoding = encoding
        self.loop = loop
        self.redis_global_connection = None

    @asyncio.coroutine
    def _get_connection(self):
        """
        create new Redis connection
        for more details see create_redis function in aioredis module
        this function is coroutine
        """
        connection = yield from aioredis.create_redis(
            self.address,
            db=self.db,
            password=self.password,
            ssl=self.ssl,
            encoding=self.encoding,
            loop=self.loop
        )
        return connection

    @asyncio.coroutine
    def init(self):
        """
        create new Redis global connection
        this function is coroutine
        """
        print("create new Redis instance")
        self.redis_global_connection = yield from self._get_connection()

    @asyncio.coroutine
    def get_sub_connection(self):
        """
        create new connection as subscribe connection to Redis server
        this function is coroutine
        """
        sub_connection = yield from self._get_connection()

        return sub_connection