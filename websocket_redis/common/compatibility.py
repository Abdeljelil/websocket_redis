try:
    import asyncio

    # Replace with BaseEventLoop.create_task when dropping Python < 3.4.2.
    try:                                                # pragma: no cover
        asyncio_ensure_future = asyncio.ensure_future   # Python ≥ 3.5
    except AttributeError:                              # pragma: no cover
        asyncio_ensure_future = asyncio.async           # Python < 3.5

except ImportError:
    # python prior to 3.3
    asyncio_ensure_future = None
