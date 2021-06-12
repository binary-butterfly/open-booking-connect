# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import json
from enum import Enum
from decimal import Decimal
from datetime import datetime
from dataclasses import is_dataclass, asdict


class DefaultJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, Enum):
            return obj.name
        if is_dataclass(obj):
            return asdict(obj)
        return obj.__dict__
