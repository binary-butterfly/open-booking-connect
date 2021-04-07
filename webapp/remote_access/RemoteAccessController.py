# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from quart import Blueprint
from ..models import Resource
from ..common.response import jsonify_error, jsonify_success
from ..websocket_connect.WebsocketQueue import put_request
from ..common.enums import MessageType, ResourceStatus, RemoteChangeResourceStatus

remote_access = Blueprint('remote_access', __name__, template_folder='templates')


@remote_access.route('/backend/resource/<int:remote_resource_id>/change-status/<status>')
async def backend_resource_change_status(remote_resource_id, status):
    if not hasattr(ResourceStatus, status):
        return jsonify_error()
    resource = await Resource.filter(remote_id=remote_resource_id).first()
    if not resource:
        return jsonify_error()
    await put_request(
        resource.id,
        MessageType.RemoteChangeResourceStatus,
        RemoteChangeResourceStatus(
            uid=resource.uid,
            status=getattr(ResourceStatus, status)
        )
    )
    return jsonify_success()
