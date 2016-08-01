#!/usr/bin/env python

import asyncio
import websockets
import os
import sys
import ssl

websocket = None

os.environ['PYTHONASYNCIODEBUG'] = '1'


@asyncio.coroutine
def send(websocket):
    print('in send')
    try:
        i = 0
        while True:
            yield from asyncio.sleep(1)
            yield from websocket.send("from client")
            print("send to server {}".format(i))

    finally:
        yield from websocket.close()


@asyncio.coroutine
def recv(websocket):
    print("in revieve")
    try:
        while True:
            greeting = yield from websocket.recv()
            print("< {}".format(greeting))

    finally:
        yield from websocket.close()

if __name__ == "__main__":

    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    # context.load_verify_locations("./ssl/cert.pem")

    context.verify_mode = ssl.CERT_NONE

    client = sys.argv[1]
    coroutine_con = websockets.connect(
        'wss://localhost:5678/ws/{}'.format(client),
        ssl=context)
    task_con = asyncio.async(coroutine_con)
    asyncio.get_event_loop().run_until_complete(task_con)

    websocket = task_con.result()

    send_task = send(websocket)
    resv_task = recv(websocket)
    tasks = asyncio.wait([send_task, resv_task])
    asyncio.get_event_loop().run_until_complete(tasks)
