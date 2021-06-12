# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from hashlib import sha256
from functools import wraps
from secrets import compare_digest

from quart import abort, current_app, request


def auth_required(*users):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            auth = request.authorization
            if auth is None or auth.type != "basic":
                abort(403)
            if auth.username not in users or auth.username not in current_app.config['BASICAUTH']:
                abort(403)
            if not compare_digest(sha256(auth.password.encode()).hexdigest(), current_app.config["BASICAUTH"][auth.username]):
                abort(403)

            return await func(*args, **kwargs)
        return wrapped
    return wrapper
