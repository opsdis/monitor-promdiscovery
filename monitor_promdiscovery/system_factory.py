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
import monitor_promdiscovery.icinga2 as Icinga2
import monitor_promdiscovery.monitor as Monitor
from monitor_promdiscovery.hosts_by_hostgroup import HostByGroup


def select_system(system: str) -> HostByGroup:
    supported_system = {'icinga2': Icinga2.Icinga2Config,
                        'op5monitor': Monitor.MonitorConfig}
    return supported_system.get(system, None)
