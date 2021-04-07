# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from enum import Enum
from dataclasses import dataclass


class Connection(Enum):
    online = 'online'
    offline = 'offline'


class MessageType(Enum):
    RemoteChangeResourceStatus = 'RemoteChangeResourceStatus'
    ResourceStatusChange = 'ResourceStatusChange'
    Authorize = 'Authorize'


class ResourceStatus(Enum):
    open = 'open'
    closed = 'closed'
    unknown = 'unknown'


@dataclass
class RemoteChangeResourceStatus:
    uid: str
    status: ResourceStatus


@dataclass
class ResourceStatusChange:
    uid: str
    status: ResourceStatus


@dataclass
class RemoteChangeResourceStatusReply:
    uid: str
