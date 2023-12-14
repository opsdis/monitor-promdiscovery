[![PyPI version](https://badge.fury.io/py/monitor-promdiscovery.svg)](https://badge.fury.io/py/monitor-promdiscovery)

monitor-promdiscovery
------------------------

# Overview
The *monitor-promdiscovery* tool generate file-based service discovery files for Prometheus, for the 
[monitor-exporter](https://github.com/opsdis/monitor-exporter) and [icinga2-exporter](https://github.com/opsdis/icinga2-exporter).
The tool is typically run from cron or equivalent tool to check OP5 Monitor or Icinga2 for hosts service that should be 
scraped for performance metrics by the exporters.  
For a host to be detected, it must be a part of hostgroup(s) or servicegroup(s) that is defined in the configuration 
file. For a servicegroup(s) configuration all hosts that has at least on service in the configured servicegroup(s) will
be added.
> Servicegroups configuration is not supported for icinga2

# Flow

![Flow overview](https://github.com/opsdis/monitor-promdiscovery/raw/master/doc/overview.png)

 1. *monitor-promdiscovery* is executed at regular intervals, e.g. every minute, by cron.
 2. *monitor-promdiscovery* performs a filter query against the configured Monitor instance for all hosts that are part of a specific hostgroup. All hosts in the hostgroup(s) will be scraped for all their services' performance data
 *monitor-exporter* or *icinga2-exporter*. 
 3. *monitor-promdiscovery* checks against the configured file-based discovery if any host from the above call is new or not existing anymore.
 4. Only if there is not a match the file-based discovery file will be updated
 5. If the file is updated, Prometheus will reload the configuration file.

# Running
## Only use configuration file 

	python -m monitor_promdiscovery -f ./config.yml

## Override system property in the configuration file 

	python -m monitor_promdiscovery -f ./config.yml -s <system>
	
> Where *<system>* can be either icinga2 or monitor
	
# Installing
1. Check out / clone the git repo.
2. Install dependencies
    
    `pip install -r requirements.txt`
     
3. Build a distribution 

    `python setup.py sdist`

4. Install locally
 
    `pip install dist/monitor-promdiscovery-X.Y.Z.tar.gz`
     


# Configuration
The *monitor-promdiscovery* configuration file should be rather self-explanatory. 

>NB! Only icinga2 or op5monitor has to be configured. If both are used, use the -s switch instead of configure
>system in the property file. Using the below config executing without specifiying -s <system>, the icinga2 entry will be used.

```yaml
# The system can be either op5monitor or icinga2 
system: icinga2

op5monitor:  
  url: https://monitor.local  
  user: monitor  
  passwd: monitor  
  # Connection timeout - default 5
  # timeout: 5
  # Verify ssl - default False
  # verify: False

  # The hostgroup(s) used to select hosts as targets  
  hostgroup: 
    - prometheus
  # The servicegroup(s) used to select hosts as targets
  # Will include all hosts that has at least on service in the configured servicegroup(s)
  servicegroup:
    - servicepoint
  prometheus:  
    # path where to create the file-based discovery file - must be set  
    sd_file: <sd_directory>/monitor_sd.yml  
    # Additional labels to tag metrics with - optional
    labels:  
      source: monitor  
      env: prod

icinga2:
  url: https://127.0.0.1:5665
  user: root
  passwd: cf593406ffcfd2ef
  # Connection timeout - default 5
  # timeout: 5
  # Verify ssl - default False
  # verify: False

  # The hostgroup used to select hosts as targets
  hostgroup: 
    - prometheus
    - linux_servers
  prometheus:
    # path where to create the file-based discovery file - must be set
    sd_file: /home/andersh/programs/prometheus/sd/icinga2_sd.yml
    # Additional labels to tag metrics with - optional
    labels:
      source: icinga2
      env: prod

logger:
  # Path and name for the log file. If not set sent to stdout
  logfile: monitor-promdiscovery.log
  # Format if day will have current day as post fix
  # format: day
  # Log level
  #level: INFO

``` 

> The hostgroup property can be both a single value or a list of different hostgroups as shown above.

## Prometheus configuration
The Prometheus configuration file would typical have the following job configuration in the scrape_configs section for the *monitor-exporter*:  
```yaml

  - job_name: 'op5'
    scrape_interval: 2m
    metrics_path: /metrics
    file_sd_configs:
    - files:
      - 'sd/monitor_sd.yml'
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        # The address for the monitor-exporter
        replacement: localhost:5000

```
And the format for icinga2 is almost the same:
```yaml
  - job_name: 'icinga2'
    scrape_interval: 2m
    metrics_path: /metrics
    file_sd_configs:
    - files:
      - 'sd/icinga2_sd.yml'
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        # The address for the monitor-exporter
        replacement: localhost:5000
```

> The `file_sd_configs` must have the same filename as created by the tool, as defined in the configuration file. 

# System requirement
Python 3.6

For required packages, please review `requirements.txt`


