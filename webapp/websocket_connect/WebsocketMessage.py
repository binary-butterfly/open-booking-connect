# encoding: utf-8

"""
Giro-e TCC
Copyright (c) 2019 - 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from random import randint
from ..common.enums import MessageType
from .WebsocketQueue import put_reply
from ..models import Resource


class WebsocketMessage:
    def __init__(self, client_id, message):
        self.client_id = client_id
        self.type = getattr(MessageType, message['type'])
        self.state = message['state']
        self.uid = message['uid']
        self.data = message['data']

    async def run(self):
        if hasattr(self, 'handle%s' % self.type.name):
            await getattr(self, 'handle%s' % self.type.name)()

    async def reply(self, data: dict):
        await put_reply(self.client_id, self.type, self.uid, data)

    async def handleBootNotification(self):
        await self.reply({})

    async def handleAuthorize(self):
        await self.reply({
            'status': 'ok',
            'request_uid': self.data['request_uid'],
            'resource_uid': 'resource-%s' % randint(1, 4)
        })

    async def handleDoorStatus(self):
        await self.reply({})

    async def handleConnectionChange(self):
        await self.reply({})

    async def handleException(self):
        await self.reply({})

    async def handleResourceStatusChange(self):
        resource = await Resource.filter(uid=self.data['resource_uid']).first()
        if not resource:
            await self.reply({
                'status': 'error'
            })
            return
        resource.status = self.data['status']
        await resource.save()
        await self.reply({
            'status': 'ok'
        })
