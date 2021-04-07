# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import os


class BaseConfig:
    INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

    PROJECT_NAME = "openbikebox-connect"
    PROJECT_VERSION = '0.1.0'

    DEBUG = False
    TESTING = False

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    LOG_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir, 'logs'))
