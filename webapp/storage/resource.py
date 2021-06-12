# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from tortoise.models import Model
from tortoise import fields
from ..common.enums import ResourceStatus
from .base import Base


class Resource(Model, Base):
    class Meta:
        table = "resource"

    db_fields = [
        'created', 'modified', 'uid', 'remote_id', 'status', 'client_id'
    ]

    db_field_datetime = [
        'created', 'modified'
    ]
    db_field_enum = [
        'status'
    ]

    id = fields.BigIntField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    uid = fields.CharField(max_length=255, index=True, null=True, default=None)
    client_id = fields.BigIntField()
    remote_id = fields.BigIntField(null=True, default=None)
    status = fields.CharEnumField(enum_type=ResourceStatus, null=True, default=None)
