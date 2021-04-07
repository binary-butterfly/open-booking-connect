# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from quart import Quart
from aioredis import create_redis


class Redis:
    redis_queue_url = None
    _redis = None

    def init_app(self, app: Quart) -> None:
        self.redis_queue_url = app.config.get('REDIS_URL', 'localhost')
        app.before_serving(self._before_serving)
        app.after_serving(self._after_serving)

    async def _before_serving(self) -> None:
        self._redis = await create_redis(self.redis_queue_url)

    async def manual_close(self) -> None:
        await self._after_serving()

    async def _after_serving(self) -> None:
        self._redis.close()
        await self._redis.wait_closed()
        self._redis = None

    async def get(self, db, key):
        if not self._redis:
            await self._before_serving()
        result = await self._redis.hget(db, key)
        if result:
            return result.decode()

    async def set(self, db, key, value):
        if not self._redis:
            await self._before_serving()
        await self._redis.hset(db, key, value)

    async def increment(self, db, key):
        await self._redis.hincrby(db, key)

    async def remove(self, db, key):
        if not self._redis:
            await self._before_serving()
        await self._redis.hdel(db, key)

    async def scan(self, db):
        if not self._redis:
            await self._before_serving()
        result = {}
        for key, value in (await self._redis.hgetall(db)).items():
            result[key] = value
        return result
