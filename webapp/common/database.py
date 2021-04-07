# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from quart import Quart
from tortoise import Tortoise


class QuartDatabase:
    def init_app(self, app: Quart) -> None:
        self.database_uri = app.config["QUART_DATABASES_URI"]
        app.before_serving(self.connect)
        app.after_serving(self._after_serving)

    async def connect(self) -> None:
        await Tortoise.init(
            db_url=self.database_uri,
            modules={'models': ['webapp.models']}
        )

    async def _after_serving(self) -> None:
        await Tortoise.close_connections()

    async def close(self):
        await Tortoise.close_connections()
