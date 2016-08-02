import redis


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
