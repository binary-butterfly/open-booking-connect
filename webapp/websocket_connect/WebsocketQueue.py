# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import json
import asyncio
from uuid import uuid4
from typing import Union
from dataclasses import dataclass
from quart import copy_current_app_context
from ..extensions import queue, redis, logger, connected_websockets
from ..common.enums import MessageType
from ..common.misc import DefaultJSONEncoder


async def put_request(client_id: int, message_type: MessageType, data: Union[dict, dataclass]):
    @copy_current_app_context
    async def check_reply_delay(client_id: int, message_type: MessageType, message_uid: str):
        await check_reply(client_id, message_type, message_uid)

    message_uid = str(uuid4())
    websocket_client_uid = await connected_websockets.get(client_id)
    if not websocket_client_uid:
        return
    if type(data) is dataclass:
        data = data.asdict()
    await queue.put_sub(
        websocket_client_uid,
        json.dumps({
            'type': message_type.name,
            'uid': message_uid,
            'data': data,
            'state': 'request'
        }, cls=DefaultJSONEncoder)
    )
    await redis.set('message-uid', message_uid, message_type.name)
    asyncio.ensure_future(check_reply_delay(client_id, message_type, message_uid))


async def check_reply(client_id: int, message_type: MessageType, message_uid: str):
    await asyncio.sleep(60)
    message_check = await redis.get('message-uid', message_uid)
    if not message_check:
        return
    logger.info(
        'websocket.connection',
        'timeout at client %s message %s %s' % (client_id, message_type.name, message_uid)
    )
    await redis.remove('message-uid', message_uid)


async def put_reply(client_id: int, message_type: MessageType, message_uid: str, data: dict):
    websocket_client_uid = await connected_websockets.get(client_id)
    if not websocket_client_uid:
        return
    await queue.put_sub(
        websocket_client_uid,
        json.dumps({
            'type': message_type.name + 'Reply',
            'uid': message_uid,
            'data': data,
            'state': 'reply'
        }, cls=DefaultJSONEncoder)
    )



