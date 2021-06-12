# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from typing import Union
from .redis import Redis


class RedisWrapper:
    def __init__(self, redis: Redis, database: str):
        self.redis = redis
        self.database = database

    async def get(self, key: Union[str, int]) -> Union[str, None]:
        result = await self.redis.get(self.database, str(key))
        if result is None:
            return None
        return result

    async def set(self, key: Union[str, int], value: Union[str]):
        return await self.redis.set(self.database, str(key), value)

    async def remove(self, key: Union[str, int]):
        return await self.redis.remove(self.database, str(key))
