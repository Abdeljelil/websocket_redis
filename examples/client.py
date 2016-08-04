#!/usr/bin/env python

import asyncio
import websockets
import sys

websocket = None


@asyncio.coroutine
def send(websocket):
    print('in send')
    try:
        i = 0
        while True:
            yield from asyncio.sleep(2)
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

    client = sys.argv[1]
    coroutine_con = websockets.connect(
        'ws://localhost:5678/ws/{}'.format(client))
    task_con = asyncio.async(coroutine_con)
    asyncio.get_event_loop().run_until_complete(task_con)

    websocket = task_con.result()

    send_task = send(websocket)
    resv_task = recv(websocket)
    tasks = asyncio.wait([send_task, resv_task])
    asyncio.get_event_loop().run_until_complete(tasks)
