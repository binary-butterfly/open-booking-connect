# encoding: utf-8

"""
open booking connect
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from dateutil.parser import parse as dateutil_parse


class Base:
    db_fields = []
    db_field_datetime = []

    def to_dict(self):
        result = {}
        for field in self.db_fields:
            result[field] = getattr(self, field)
        return result

    def from_dict(self, data):
        for field in self.db_fields:
            if field in data:
                if field in self.db_field_datetime:
                    setattr(self, field, dateutil_parse(data[field]) if data[field] else None)
                else:
                    setattr(self, field, data[field])
