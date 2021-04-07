# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from quart import Quart
from aio_pika import connect_robust, Message


class AmpqQueue:
    _connection = None
    channel = None

    def init_app(self, app: Quart) -> None:
        app.before_serving(self._before_serving)
        app.after_serving(self._after_serving)

    async def _before_serving(self) -> None:
        from quart import current_app
        self._connection = await connect_robust(current_app.config['AMQP_QUEUE'])
        self.channel = await self._connection.channel()

    async def _after_serving(self) -> None:
        if self._connection is None:
            return
        await self._connection.close()
        self._redis = None

    async def put_sub(self, key: str, item: str) -> None:
        if not self._connection or not self.channel:
            await self._before_serving()
        await self.channel.default_exchange.publish(
            Message(item.encode()),
            routing_key=key,
            timeout=120
        )
