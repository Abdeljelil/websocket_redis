import asyncio
from websocket_redis.server import WSServer


ws_connection = dict(
    host="127.0.0.1",
    port=5678)

redis_connection = dict(
    address=("localhost", 6379)
)

loop = asyncio.get_event_loop()

loop.run_until_complete(WSServer.run_server(
    ws_connection, redis_connection, app_name="my_app"))
loop.run_forever()
loop.close()
