import asyncio
import aioredis
import logging


logger = logging.getLogger(__name__)


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

        self._connections = []

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

    def _wait_closed(self, connection):
        loop = asyncio.get_event_loop()
        try:

            loop.run_until_complete(
                asyncio.wait_for(
                    connection.wait_closed(),
                    timeout=1))
        except asyncio.TimeoutError:
            logger.warning("redis connectin failed to stop")

    def close(self):

        if self.redis_global_connection.closed is False:
            logger.info("closing global redis connection")
            self.redis_global_connection.close()
            self._wait_closed(self.redis_global_connection)
        for connection in self._connections:
            if connection.closed is False:
                logger.info("closing push/sub redis connection")
                self.connection.close()
                self._wait_closed(self.connection)

    @asyncio.coroutine
    def init(self):
        """
        create new Redis global connection
        this function is coroutine
        """

        self.redis_global_connection = yield from self._get_connection()

    @asyncio.coroutine
    def get_sub_connection(self):
        """
        create new connection as subscribe connection to Redis server
        this function is coroutine
        """
        sub_connection = yield from self._get_connection()
        self._connections.append(sub_connection)
        return sub_connection
