# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import json
import pytz
import random
import string
from typing import Union
from datetime import datetime, timedelta
from .misc import DefaultJSONEncoder


def get_random_password(length=16):
    return ''.join(random.SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits
    ) for _ in range(length))


def get_current_time():
    return datetime.utcnow()
