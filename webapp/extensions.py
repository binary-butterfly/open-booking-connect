# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from .common.database import QuartDatabase
db = QuartDatabase()

from .common.logger import Logger
logger = Logger()

from .common.requests import Requests
requests = Requests()

from .common.amqp_queue import AmpqQueue
queue = AmpqQueue()

from .common.redis import Redis
redis = Redis()

from .common.redis_wrapper import RedisWrapper
connected_websockets = RedisWrapper(redis, 'connected_websockets')
