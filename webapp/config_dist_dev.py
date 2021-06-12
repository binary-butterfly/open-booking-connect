# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from .common.constants import BaseConfig


class Config(BaseConfig):
    PROJECT_URL = 'http://URL'

    SECRET_KEY = 'RANDOM-KEY'
    QUART_DATABASES_URI = 'mysql://root:root@mysql/connect'

    REDIS_URL = 'redis://redis'
    AMQP_QUEUE = 'amqp://rabbitmq'

