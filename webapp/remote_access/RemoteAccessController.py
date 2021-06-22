# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from datetime import date, timedelta
from tortoise.query_utils import Q
from quart import Blueprint, request
from ..models import Resource, Message
from ..common.response import jsonify_error, jsonify_success
from ..websocket_connect.WebsocketQueue import put_request
from ..common.enums import MessageType, ResourceStatus, RemoteChangeResourceStatus
from ..common.basicauth import auth_required

remote_access = Blueprint('remote_access', __name__, template_folder='templates', url_prefix='/api/v1/backend')


@auth_required()
@remote_access.route('/resource/<int:remote_resource_id>/change-status/<status>')
async def backend_resource_change_status(remote_resource_id, status):
    if not hasattr(ResourceStatus, status):
        return await jsonify_error('invalid status')
    resource = await Resource.filter(remote_id=remote_resource_id).first()
    if not resource:
        return await jsonify_error('invalid resource')
    await put_request(
        resource.id,
        MessageType.RemoteChangeResourceStatus,
        RemoteChangeResourceStatus(
            uid=resource.uid,
            status=getattr(ResourceStatus, status)
        )
    )
    return jsonify_success()


@auth_required()
@remote_access.route('/client/<int:resource_id>/messages')
async def backend_api_messages(resource_id):
    resource = await Resource.filter(remote_id=resource_id).first()
    if not resource:
        return jsonify_error()
    items_per_page = request.args.get('items_per_page', 25, type=int)
    page = request.args.get('page', 1, type=int)

    messages = Message.filter(client_id=resource.client_id)
    if request.args.get('begin'):
        messages = messages.filter(Q(created__gt=date.fromisoformat(request.args.get('begin'))))
    if request.args.get('end'):
        messages = messages.filter(Q(created__lt=date.fromisoformat(request.args.get('end')) + timedelta(days=1)))
    count = await messages.count()
    messages = messages.order_by('-id')\
        .limit(items_per_page)\
        .offset((page - 1) * items_per_page)\
        .all()
    return jsonify_success([message.to_dict() for message in await messages], count=count)
