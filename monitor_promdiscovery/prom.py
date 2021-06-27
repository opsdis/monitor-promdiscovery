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
import os

import yaml

import monitor_promdiscovery.log as log


class PromDis(object):

    def __init__(self, config, monitor_hosts: list):
        if 'system' in config:
            system = config['system']
            self.file_name = config[system]['prometheus']['sd_file']
            if 'labels' in config[system]['prometheus']:
                self.labels = config[system]['prometheus']['labels']
            else:
                self.labels = {}

        self.monitor_hosts = monitor_hosts
        self.prom_targets = []
        self.set_of_targets = set()
        self.set_of_monitor_hosts = set()
        self.existing_labels = {}

        if os.path.exists(self.file_name):
            yml = yaml.load(open(self.file_name), Loader=yaml.SafeLoader)
            if yml and 'targets' in yml[0]:
                self.prom_targets = yml[0]['targets']
                self.set_of_targets = set(self.prom_targets)
                if 'labels' in yml[0]:
                    self.existing_labels = yml[0]['labels']

        if monitor_hosts:
            self.set_of_monitor_hosts = set(self.monitor_hosts)

    def match(self) -> bool:
        """
        Match if the current target hosts are the same as the one you got from Monitor
        :return:
        """
        if self.set_of_targets == self.set_of_monitor_hosts and \
                self.existing_labels == self.labels:
            log.info(
                "Monitor and service discovery file match - {} target entries".format(len(self.set_of_monitor_hosts)))
            return True
        log.info(
            "Monitor and service discovery file not match - {} target entries in Monitor and {} entries in service discovery".format(
                len(self.set_of_monitor_hosts), len(self.set_of_targets)))
        return False

    def update_targets(self):
        """
        Write a new sd_file
        :return:
        """
        try:
            with open(self.file_name, 'w') as filetowrite:
                targets = {'labels': self.labels, 'targets': sorted(self.monitor_hosts)}
                targets_list = [targets]
                yaml.dump(targets_list, filetowrite, default_flow_style=False)
                log.info("Service discovery file created {}".format(self.file_name))
        except Exception as err:
            log.error("{}".format(str(err)))
            raise err
