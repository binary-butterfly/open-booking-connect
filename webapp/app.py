# encoding: utf-8

"""
openbikebox connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""


import os
import traceback
from quart import Quart, jsonify

from webapp.config import Config
from .common.filter import register_global_filters
from .extensions import db, requests, queue, redis

# Blueprints
from .websocket_connect import websocket_connect
from .remote_access import remote_access

__all__ = ['launch']

BLUEPRINTS = [
    websocket_connect,
    remote_access
]


def launch():
    app = Quart(
        Config.PROJECT_NAME,
        instance_path=Config.INSTANCE_FOLDER_PATH,
        instance_relative_config=True,
        template_folder=os.path.join(Config.PROJECT_ROOT, 'templates')
    )
    configure_app(app)
    configure_blueprints(app)
    configure_extensions(app)
    configure_logging(app)
    configure_filters(app)
    configure_error_handlers(app)
    return app


def configure_app(app):
    app.config.from_object(Config)
    app.config['MODE'] = os.getenv('APPLICATION_MODE', 'DEVELOPMENT')
    print("Running in %s mode" % app.config['MODE'])


def configure_extensions(app):
    db.init_app(app)
    requests.init_app(app)
    queue.init_app(app)
    redis.init_app(app)


def configure_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)


def configure_filters(app):
    register_global_filters(app)


def configure_logging(app):
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])


def configure_error_handlers(app):
    @app.errorhandler(400)
    async def error_400(error):
        return jsonify({
            'status': -1,
            'error': 400
        }), 400

    @app.errorhandler(403)
    async def error_403(error):
        return jsonify({
            'status': -1,
            'error': 403
        }), 403

    @app.errorhandler(404)
    async def error_404(error):
        return jsonify({
            'status': -1,
            'error': 404
        }), 404

    @app.errorhandler(500)
    async def error_500(error):
        from .extensions import logger
        logger.critical('app', str(error), traceback.format_exc())
        return jsonify({
            'status': -1,
            'error': 500
        }), 500

    if not app.config['DEBUG']:
        @app.errorhandler(Exception)
        async def internal_server_error(error):
            from .extensions import logger
            logger.critical('app', str(error), traceback.format_exc())
            return jsonify({
                'status': -1,
                'error': 500
            }), 500
