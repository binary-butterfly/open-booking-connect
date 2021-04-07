# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from typing import Callable, Any
from functools import wraps
from quart.cli import ScriptInfo


def create_cli_app_context(func: Callable) -> Callable:

    @wraps(func)
    def wrapper(info: ScriptInfo, *args: Any, **kwargs: Any) -> Any:
        app = info.load_app()
        context = {}
        context.update(app.make_shell_context())
        return func(app, *args, **kwargs)

    return wrapper


def cli_app_context(func: Callable) -> Callable:

    @wraps(func)
    async def wrapper(app, *args: Any, **kwargs: Any) -> Any:
        async with app.app_context():
            return await func(*args, **kwargs)

    return wrapper


