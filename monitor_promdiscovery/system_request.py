# -*- coding: utf-8 -*-
"""
    Copyright (C) 2019  Opsdis AB

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
import json
import time
from typing import Dict, Any

import requests
from requests.auth import HTTPBasicAuth

import monitor_promdiscovery.log as log
from monitor_promdiscovery.http_connection import HttpConnection as Connection

requests.packages.urllib3.disable_warnings()


class SystemRequest:

    def __init__(self, connection: Connection):
        self.connection = connection

    def get(self, path):
        """
        Make a get call to Monitor
        :param path:
        :return:
        """
        start_time = time.time()
        try:
            url = self.connection.url + path
            data_from_system = requests.get(url,
                                            auth=HTTPBasicAuth(self.connection.user, self.connection.passwd),
                                            headers=self.connection.headers,
                                            verify=self.connection.verify, timeout=self.connection.timeout)

            data_from_system.raise_for_status()

            if data_from_system.status_code != 200 and data_from_system.status_code != 201:
                log.warn("Not a valid response - {}:{}".format(str(data_from_system.content),
                                                               data_from_system.status_code))
            else:
                log.info("call api {}".format(url), {'status': data_from_system.status_code, 'method': 'GET',
                                                     'response_time': data_from_system.elapsed.total_seconds()})
            return data_from_system.content

        except requests.exceptions.HTTPError as err:
            log.warn("{}".format(str(err)))
            raise err
        except requests.exceptions.RequestException as err:
            log.warn("{}".format(str(err)))
            raise err
        finally:
            request_time = int((time.time() - start_time) * 1000) / 1000
            log.info_response_time("Response time {}".format(self.connection.url), request_time)

    def post(self, path: str, body: Dict[str, Any]) -> bytes:
        start_time = time.time()
        url = self.connection.url + path
        try:
            data_from_system = requests.post(url, auth=HTTPBasicAuth(self.connection.user, self.connection.passwd),
                                             verify=self.connection.verify,
                                             headers=self.connection.headers,
                                             data=json.dumps(body), timeout=self.connection.timeout)

            data_from_system.raise_for_status()

            if data_from_system.status_code != 200 and data_from_system.status_code != 201:
                log.warn("Not a valid response - {}:{}".format(str(data_from_system.content),
                                                               data_from_system.status_code))
            else:
                log.info("call api {}".format(url), {'status': data_from_system.status_code, 'method': 'POST',
                                                     'response_time': data_from_system.elapsed.total_seconds()})
            return data_from_system.content

        except requests.exceptions.HTTPError as err:
            log.warn("{}".format(str(err)))
            raise err
        except requests.exceptions.RequestException as err:
            log.warn("{}".format(str(err)))
            raise err
        finally:
            request_time = int((time.time() - start_time) * 1000) / 1000
            log.info_response_time("Response time {}".format(self.connection.url), request_time)
