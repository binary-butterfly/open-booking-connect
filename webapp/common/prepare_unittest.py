# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import pymysql
from urllib.parse import urlparse
from quart import current_app


def prepare_unittest():
    if current_app.config['MODE'] != 'DEVELOPMENT' or not current_app.config['DEBUG']:
        print('wrong mode')
        return

    url = urlparse(current_app.config['SQLALCHEMY_DATABASE_URI'])
    connection = pymysql.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        db=url.path[1:],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        for line in truncate_dbs.split("\n"):
            if not line:
                continue
            cursor.execute(line)
    connection.commit()


truncate_dbs = '''
SET FOREIGN_KEY_CHECKS=0;
TRUNCATE `action`;
TRUNCATE `cashpoint`;
TRUNCATE `hardware`;
TRUNCATE `pricegroup`;
TRUNCATE `token`;
TRUNCATE `unit`;
SET FOREIGN_KEY_CHECKS=1;
'''
