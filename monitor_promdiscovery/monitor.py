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
import requests
import json
import monitor_promdiscovery.log as log
import time
requests.packages.urllib3.disable_warnings()


class MonitorConfig:

    def __init__(self, monitor):
        self.user = monitor['op5monitor']['user']
        self.passwd = monitor['op5monitor']['passwd']
        self.url = monitor['op5monitor']['url']
        self.headers = {'content-type': 'application/json'}
        self.verify = False
        self.hostgroup = monitor['op5monitor']['hostgroup']

    def get_auth(self):
        return (self.user, self.passwd)

    def get_header(self):
        return self.headers

    def get_verify(self):
        return self.verify

    def get_url(self):
        return self.url

    def get_labels(self):
        '''
        Get all configured additional labels that is part of the sd config
        :return:
        '''
        labeldict = {}
        for label in self.labels:
            for custom_var, value in label.items():
                for key, prom_label in value.items():
                    labeldict.update({custom_var: prom_label})
        return labeldict

    def get_hosts_by_hostgroup(self) -> list:
        '''
        Get all hosts in a specific hostgroup.
        Return from Monitor is a json list e.g. [{"name":"google.se"},{"name":"sunet.se"}]
        :return:
        '''
        response_body, status = self.get(
            '/api/filter/query?query=[hosts]+groups>="{}"&columns=name&limit={}'.format(self.hostgroup, 10000))
        hosts_entries = json.loads(response_body)
        hosts = []
        for host_entry in hosts_entries:
            hosts.append(host_entry['name'])
        return hosts

    def get(self, path):
        '''
        Make a get call to Monitor
        :param path:
        :return:
        '''
        start_time = time.time()
        try:

            r = requests.get(self.get_url() + path, auth=self.get_auth(), headers=self.get_header(),
                             verify=self.get_verify())

            if r.status_code == 200 or r.status_code == 404:
                status = r.status_code
            else:
                r.raise_for_status()

            return r.content, r.status_code

        except (requests.exceptions.HTTPError) as err:
            log.warn("{}".format(str(err)))
            raise err
        except (requests.exceptions.RequestException) as err:
            log.warn("{}".format(str(err)))
            raise err
        finally:
            request_time = int((time.time() - start_time) * 1000)/1000
            log.info_response_time("Response time Monitor", request_time)