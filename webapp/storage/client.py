# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from tortoise.models import Model
from tortoise import fields
from ..common.enums import Connection
from .base import Base


class Client(Model, Base):
    class Meta:
        table = "client"

    db_fields = [
        'created', 'modified', 'remote_id', 'uid', 'connection', 'connection_change', 'ip'
    ]

    db_field_datetime = [
        'created', 'modified', 'connection_change'
    ]
    db_field_enum = [
        'connection'
    ]

    id = fields.BigIntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    access_id = fields.BigIntField(null=True, default=None)
    remote_id = fields.BigIntField(null=True, default=None)
    uid = fields.CharField(max_length=64, index=True, default=None)
    basicauth_password = fields.CharField(max_length=64, null=True, default=None)
    ip = fields.CharField(max_length=64, null=True, default=None)
    connection = fields.CharEnumField(enum_type=Connection, null=True, default=None)
    connection_change = fields.DatetimeField(null=True, default=None)
