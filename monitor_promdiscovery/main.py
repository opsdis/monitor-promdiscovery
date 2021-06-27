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
import argparse

import yaml

import monitor_promdiscovery.log as log
import monitor_promdiscovery.prom as Prom
from monitor_promdiscovery.hosts_by_hostgroup import HostByHostgroup
from monitor_promdiscovery.system_factory import select_system


def main():
    parser = argparse.ArgumentParser(description='monitor-promdiscovery')

    parser.add_argument('-f', '--configfile',
                        dest="configfile", help="Configuration file")

    parser.add_argument('-F', '--force', action="store_true",
                        dest="force", help="Force write of service discovery file")

    parser.add_argument('-s', '--system',
                        dest="system",
                        help="System to discover. Will override configuration. Supported are op5monitor and icinga2")

    args = parser.parse_args()

    if args.configfile:
        config_file = args.configfile
    else:
        config_file = 'config.yml'

    config = read_config(config_file)

    # Override system property in config
    if args.system:
        config['system'] = args.system

    log.configure_logger(config)
    log.info("Start synchronizing")

    monitor: HostByHostgroup
    if 'system' in config and select_system(config['system']):
        monitor = select_system(config['system'])(config)
    else:
        log.error("Not a valid system {}".format(config['system']))
        exit(1)

    promdis = Prom.PromDis(config, monitor.get_hosts_by_hostgroup())

    if not promdis.match() or args.force:
        promdis.update_targets()


def read_config(config_file: str) -> dict:
    """
    Read configuration file
    :param config_file:
    :return:
    """
    try:
        with open(config_file, 'r') as ymlfile:
            config = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    except (FileNotFoundError, IOError):
        print("Config file {} not found".format(config_file))
        exit(1)
    except (yaml.YAMLError, yaml.MarkedYAMLError) as err:
        print("Error will reading config file - {}".format(err))
        exit(1)

    return config
