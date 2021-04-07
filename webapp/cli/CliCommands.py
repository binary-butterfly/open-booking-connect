# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import click
import asyncio
from quart.cli import pass_script_info
from .CliHelper import create_cli_app_context
from .SyncClients import sync_clients as sync_clients_run


def register_cli_commands(cli):
    cli.add_command(sync_clients)


@click.command("sync-clients")
@pass_script_info
@create_cli_app_context
def sync_clients(app):
    asyncio.get_event_loop().run_until_complete(sync_clients_run(app))
