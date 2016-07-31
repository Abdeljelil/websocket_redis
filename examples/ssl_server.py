import asyncio
from websocket_redis.server import WSServer
import ssl

# openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days
# 300 -nodes


ws_connection = dict(
    host="127.0.0.1",
    port=5678)

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_cert_chain(certfile="./ssl/cert.pem",
                        keyfile="./ssl/key.pem")

redis_connection = dict(
    address=("localhost", 6397),
    ssl=context)

loop = asyncio.get_event_loop()

loop.run_until_complete(WSServer.run_server(
    ws_connection, redis_connection))
loop.run_forever()
loop.close()
