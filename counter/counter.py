import logging

import fastapi
import redis.asyncio as redis

log = logging.getLogger(__name__)


class Counter:
    __slots__ = ("_conn", "_key", "_lock")

    def __init__(
        self, redis_dsn: str, count_key: str = "COUNT", lock_name: str = "COUNTER_LOCK"
    ) -> None:
        connection = redis.Redis.from_url(redis_dsn)
        self._conn = connection
        self._key = count_key
        self._lock = connection.lock(lock_name)

    async def increment(self, amount: int = 1) -> int:
        async with self._lock:
            result = await self._conn.incr(name=self._key, amount=amount)
            return int(result)

    async def decrement(self, amount: int = 1) -> int:
        async with self._lock:
            result = await self._conn.decr(name=self._key, amount=amount)
            return int(result)

    async def get(self) -> int:
        async with self._lock:
            result = await self._conn.get(self._key)
            if result is None:
                log.info("no value set for %s, returning 0", self._key)
                return 0
            return int(result)


def middleware(counter: Counter):
    async def __(request: fastapi.Request, call_next) -> fastapi.Response:
        request.state.counter = counter
        response = await call_next(request)
        return response

    return __


def get_counter(request: fastapi.Request) -> Counter:
    return request.state.counter
