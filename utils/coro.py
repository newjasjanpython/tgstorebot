import asyncio
import functools
import time
from contextlib import contextmanager


__all__ = ['sync_to_async', 'use_sync']


def sync_to_async(func):
    @contextmanager
    def wrapping_logic():
        start_ts = time.time()
        yield
        dur = time.time() - start_ts
        print('{} took {:.2} seconds'.format(func.__name__, dur))

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:
            with wrapping_logic():
                return (await func(*args, **kwargs))
    return wrapper


async def use_sync(func, executor=None):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, func)
