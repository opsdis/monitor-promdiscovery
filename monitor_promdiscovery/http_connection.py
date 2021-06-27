# -*- coding: utf-8 -*-
"""
    Copyright (C) 2021  Opsdis AB

    This file is part of monitor-exporter.

    monitor-promdiscovery is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    monitor-promdiscovery is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with monitor-exporter.  If not, see <http://www.gnu.org/licenses/>.

"""


class HttpConnection:

    def __init__(self):
        self.url = ''
        self.user = ''
        self.passwd = ''
        self.timeout = 5
        self.headers = {'content-type': 'application/json'}
        self.verify = False


def factory(prefix: str, config: dict) -> HttpConnection:
    connection = HttpConnection()
    connection.url = config[prefix]['url']
    connection.user = config[prefix]['user']
    connection.passwd = config[prefix]['passwd']

    connection.timeout = 5
    if 'timeout' in config[prefix]:
        connection.timeout = config[prefix]['timeout']

    connection.verify = False
    if 'verify' in config[prefix]:
        connection.verify = config[prefix]['verify']

    return connection
