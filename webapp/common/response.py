# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from typing import Union
from quart import jsonify


def jsonify_success(data: Union[dict, list, str, None] = None, count: int = None):
    result = {
        'status': 0,
        'data': data
    }
    if count is not None:
        result['count'] = count
    return result


async def jsonify_error(error_dict: Union[dict, str, None] = None):
    return {
        'status': -1,
        'error': error_dict
    }
