| |cversion| |versions| |status| |codecov| |build| |health|

Websocket_redis
=============
``websocket_redis`` is an asynchronous python module gather two projects `websockets <https://github.com/aaugustin/websockets>`_ and `aioredis <https://github.com/aio-libs/aioredis>`_ to make the communication between the client and backend as easy as possible without losing any message has been sent from the client.

=============
Installation
=============

Install from Pypi:
________________________

.. code-block:: bash

    $ pip install websocket_redis

Manual installation:
________________________

.. code-block:: bash
    
    # we assume you already created the python virtualenv
    # get the latst version from master branch
    $ wget -O websocket_redis.zip https://github.com/Abdeljelil/websocket_redis/archive/master.zip
    $ unzip websocket_redis.zip
    $ cd websocket_redis-master
    $ make install
    # run tests (optional)
    $ pip install nose
    $ make test
    
`pypi <https://pypi.python.org/pypi/websocket_redis>`_.

Usage examples
--------------

Override WSHandler Methodes:

.. code:: python

    import asyncio
    from websocket_redis.server.ws_server import WSServer
    from websocket_redis.server.ws_handler import WSHandler
    
    
    class MyWSHandler(WSHandler):
    
        @asyncio.coroutine
        def on_close(self, code):
    
            print("Session {} has closed, client : {}".format(
                self.session_id, self.client))
    
        @asyncio.coroutine
        def on_error(self, e):
    
            print("Exception {} has raised, client : {}".format(
                e, self.client))
    
        @asyncio.coroutine
        def on_message(self, text):
    
            print("Message \'{}\' has received from client : {}".format(
                text, self.client))
    
        @asyncio.coroutine
        def on_send(self, text):
    
            print("Message \'{}\' will be sent to {}".format(
                text, self.client))

Start Websocker server:

.. code:: python

    ws_connection = dict(
        host="127.0.0.1",
        port=5678)

    redis_connection = dict(
        address=("localhost", 6379)
    )

    loop = asyncio.get_event_loop()
    server = WSServer(
        ws_connection=ws_connection,
        redis_connection=redis_connection,
        app_name="test_app",
        ws_handler_class=MyWSHandler
    )

    try:
        loop.run_until_complete(server.run())
        loop.run_forever()
    except KeyboardInterrupt:
        server.close()
        loop.close()

Async API:

.. code:: python

    import asyncio
    
    from websocket_redis.api.async import APIClientListener


    class MyAPIClientListener(APIClientListener):
    
        @asyncio.coroutine
        def on_message(self, message):
    
            print("new message {}".format(message.text))
            yield from message.reply("Hi!")

    redis_connection = dict(
        address=("localhost", 6379)
    )
    handler = MyAPIClientListener(redis_connection, app_name="test_app")
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(handler.run())

Threaded API:

.. code:: python

    from websocket_redis.api.threading import APIClientListener
    
    
    class MyAPIClientListener(APIClientListener):
    
        def on_message(self, message):
    
            print("new message {}".format(message.text))
            message.reply("Hi!")
    
        redis_connection = dict(
            host="localhost",
            port=6379
        )
        handler = MyAPIClientListener(redis_connection, app_name="test_app")
    
        handler.run()

.. |build| image:: https://travis-ci.org/Abdeljelil/websocket_redis.svg?branch=master
    :target: https://travis-ci.org/Abdeljelil/websocket_redis
    :alt: Travis-ci build
.. |cversion| image:: https://img.shields.io/pypi/v/websocket_redis.svg
    :target: https://pypi.python.org/pypi/websocket_redis
    :alt: Python versions supported
.. |versions| image:: https://img.shields.io/pypi/pyversions/websocket_redis.svg
    :target: https://pypi.python.org/pypi/websocket_redis
    :alt: Python versions supported
.. |codecov| image:: https://codecov.io/gh/Abdeljelil/websocket_redis/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Abdeljelil/websocket_redis
    :alt: Coverage!
.. |status| image:: https://img.shields.io/pypi/status/websocket_redis.svg
    :target: https://pypi.python.org/pypi/websocket_redis
    :alt: Package stability
.. |health| image:: https://landscape.io/github/Abdeljelil/websocket_redis/master/landscape.svg?style=flat
    :target: hhttps://landscape.io/github/Abdeljelil/websocket_redis
    :alt: Package health
