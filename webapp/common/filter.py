# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from .misc import DefaultJSONEncoder


def register_global_filters(app):
    app.json_encoder = DefaultJSONEncoder
