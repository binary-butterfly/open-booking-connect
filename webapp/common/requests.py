# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import json
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError, ClientOSError, ContentTypeError
from quart import Quart
from typing import Union
from .misc import DefaultJSONEncoder
from ..extensions import logger


class Requests:
    initialized = False

    def init_app(self, app: Quart) -> None:
        app.before_serving(self._before_serving)
        app.after_serving(self._after_serving)

    async def _before_serving(self) -> None:
        self.session = aiohttp.ClientSession()
        self.initialized = True

    async def _after_serving(self) -> None:
        await self.session.close()

    async def close(self):
        await self.session.close()

    async def get(self, url: str, log_file: str, log_message: str, auth: Union[tuple, None] = None, headers: Union[dict, None] = None):
        if not self.initialized:
            await self._before_serving()

        kwargs = {}
        if auth:
            kwargs['auth'] = aiohttp.BasicAuth(auth[0], auth[1])
        if headers:
            kwargs['headers'] = headers
        try:
            async with self.session.get(url, **kwargs) as response:
                if response.content_type == 'application/json':
                    return await response.json()
                return await response.text()
        except (ClientConnectorError, ClientOSError, ContentTypeError):
            logger.info(log_file, log_message)

    async def post(self, url: str, data: str, log_file: str, log_message: str, auth: Union[tuple, None] = None, headers: Union[dict, None] = None):
        if not self.initialized:
            await self._before_serving()
        kwargs = {}
        if not headers:
            headers = {}
        if type(data) in [dict, list]:
            kwargs['data'] = json.dumps(data, cls=DefaultJSONEncoder)
            headers['Content-Type'] = 'application/json'
        else:
            kwargs['data'] = data
        if auth:
            kwargs['auth'] = aiohttp.BasicAuth(auth[0], auth[1])
        if headers is not {}:
            kwargs['headers'] = headers
        try:
            async with self.session.post(url, **kwargs) as response:
                if response.status != 200:
                    logger.info(log_file, 'bad status code %s: %s' % (response.status, await response.text()))
                    return None
                if response.content_type == 'application/json':
                    return await response.json()

                return await response.text()
        except (ClientConnectorError, ClientOSError, ContentTypeError):
            logger.info(log_file, log_message)
