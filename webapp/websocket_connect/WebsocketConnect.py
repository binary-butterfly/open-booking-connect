# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import json
import asyncio
import traceback
from base64 import b64decode
from datetime import datetime
from hashlib import sha256
from quart import Blueprint, websocket, abort, current_app, copy_current_app_context
from ..extensions import queue, logger, connected_websockets, redis
from ..storage import Client
from ..common.enums import Connection
from .WebsocketMessage import WebsocketMessage

websocket_connect = Blueprint('websocket_connect', __name__)


@websocket_connect.websocket('/connect/<client_uid>')
async def connect_client(client_uid: str):
    if not current_app.config['DEBUG'] and not websocket.headers.get('X-Forwarded-For'):
        abort(403)
    client = await Client.filter(uid=client_uid).first()
    if not client or not websocket.headers.get('Authorization'):
        abort(403)
    credentials = b64decode(websocket.headers.get('Authorization')[6:]).decode().split(':')
    if len(credentials) != 2:
        abort(403)
    if not client.basicauth_password or sha256(credentials[1].encode()).hexdigest() != client.basicauth_password:
        abort(403)
    client.ip = websocket.headers.get('X-Forwarded-For', None)
    client.connection = Connection.online
    client.connection_change = datetime.utcnow()
    await client.save()

    websocket_client_uid_raw = None
    for key, value in websocket.headers:
        if key.lower() == 'sec-websocket-key':
            websocket_client_uid_raw = value
    if not websocket_client_uid_raw:
        abort(403)
    websocket_client_uid = b64decode(websocket_client_uid_raw).hex()
    await websocket.accept()

    logger.info('websocket', 'client %s connected with guid %s' % (client.id, websocket_client_uid))
    old_websocket_client_uid = await connected_websockets.get(client.id)
    if old_websocket_client_uid and old_websocket_client_uid != websocket_client_uid:
        logger.info('websocket', 'queue disconnecting old client %s connection with guid %s' % (client.id, old_websocket_client_uid))
        await queue.put_sub(old_websocket_client_uid, '0000')
    await connected_websockets.set(client.id, websocket_client_uid)

    producer = asyncio.create_task(sending(client.id, websocket_client_uid))
    consumer = asyncio.create_task(receiving(client.id))
    await asyncio.wait([producer, consumer], return_when=asyncio.FIRST_COMPLETED)
    producer.cancel()
    consumer.cancel()
    logger.info('websocket.connection', '%s with uid %s successfully disconnected' % (client.id, websocket_client_uid))
    abort(400)


async def sending(client_id: int, websocket_client_uid):
    single_queue = await queue.channel.declare_queue(websocket_client_uid, auto_delete=True)
    async for message in single_queue:
        data = message.body.decode()
        if data == '0000':
            message.ack()

            @copy_current_app_context
            async def delete_queue_delay(queue_to_delete):
                await delete_queue(queue_to_delete)

            await delete_queue_delay(single_queue)
            return
        logger.info('websocket.data', '<< %s %s %s' % (client_id, websocket_client_uid, data))
        await websocket.send(data)
        message.ack()


async def delete_queue(queue_to_delete):
    await asyncio.sleep(5)
    await queue_to_delete.delete(if_unused=False, if_empty=False)


async def receiving(client_id: int) -> None:
    while True:
        try:
            data = await websocket.receive()
        except asyncio.CancelledError:
            return
        logger.info('websocket.data', '>> %s' % data)
        await handle_message(client_id, data)


async def handle_message(client_id: int, data: str):
    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError:
        logger.error('websocket.data', 'got invalid message %s' % data)
        return
    try:
        if data['state'] == 'reply':
            await redis.remove('message-uid', data['uid'])
        wm = WebsocketMessage(client_id, data)
        await wm.run()
    except Exception as error:
        logger.error('websocket.data', 'error handling message %s: %s %s' % (data, str(error), traceback.format_exc()))

