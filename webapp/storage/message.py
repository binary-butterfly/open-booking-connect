# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import json
from tortoise.models import Model
from tortoise import fields
from ..common.enums import MessageType, MessageState
from webapp.common.misc import DefaultJSONEncoder
from .base import Base


class Message(Model, Base):
    class Meta:
        table = "message"

    db_fields = [
        'id', 'created', 'modified', 'client_id', 'uid', 'type', 'state', 'data'
    ]

    db_field_datetime = [
        'created', 'modified'
    ]
    db_field_enum = [
        'type'
    ]

    id = fields.BigIntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    client_id = fields.BigIntField(null=True, default=None)
    uid = fields.CharField(max_length=64, index=True, default=None)
    type = fields.CharEnumField(enum_type=MessageType, null=True, default=None)
    state = fields.CharEnumField(enum_type=MessageState, null=True, default=None)
    _data = fields.TextField(source_field='data')

    @property
    def data(self) -> dict:
        return json.loads(self._data) if self._data else {}

    @data.setter
    def data(self, data: dict):
        self._data = json.dumps(data, cls=DefaultJSONEncoder)
