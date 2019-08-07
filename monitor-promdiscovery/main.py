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
import argparse
import yaml
import prom as Prom
import monitor as Monitor
import log


def main():
    parser = argparse.ArgumentParser(description='cmdb2monitor')

    parser.add_argument('-f', '--configfile',
                        dest="configfile", help="configuration file")

    parser.add_argument('-F', '--force', action="store_true",
                    dest="force", help="force write of service discovery file")

    args = parser.parse_args()

    if args.configfile:
        config_file = args.configfile
    else:
        config_file = 'config.yml'

    config = read_config(config_file)


    #log.configure_logger("monitor-promdiscovery", 'INFO')
    log.configure_logger(config)
    log.info("Start synchronizing")
    monitor = Monitor.MonitorConfig(config)
    promdis = Prom.PromDis(config, monitor.get_hosts_by_hostgroup())

    # print (promdis.match())
    if not promdis.match() or args.force:
        promdis.update_targets()


def read_config(config_file: str) -> dict:
    '''
    Read configuration file
    :param config_file:
    :return:
    '''
    try:
        ymlfile = open(config_file, 'r')
        config = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    except (FileNotFoundError, IOError):
        print("Config file {} not found".format(config_file))
        exit(1)
    except (yaml.YAMLError, yaml.MarkedYAMLError) as err:
        print("Error will reading config file - {}".format(err))
        exit(1)

    return config
