[![Build Status](https://api.travis-ci.org/opsdis/monitor-promdiscovery.svg?branch=master)](https://api.travis-ci.org/opsdis/monitor-promdiscovery)

monitor-promdiscovery
------------------------

# Overview
The *monitor-promdiscovery* tool generate file-based service discovery files for Prometheus and the [monitor-exporter](https://bitbucket.org/opsdis/monitor-exporter). 
The tool is typical ran from cron or equivalent tools to check in Op5 Monitor for hosts service that should be scraped for performance metrics by *monitor-exporter*.  For a host to be detected it must be part of a special hostgroup, default to `monitor-exporter`, but can of course be configured.

# Flow

![Flow overview](https://bitbucket.org/opsdis/monitor-promdiscovery/raw/master/doc/overview.png)

 1. *monitor-promdiscovery* is executed on regular interval, e.g. every minute, by cron.
 2. *monitor-promdiscovery* do a filter query against configured Monitor instance for all host that is part of a specific hostgroup. All hosts in the hostgroup will by the *monitor-exporter* be scraped for all its services performance data. 
 3. *monitor-promdiscovery* check against the configured file-based discovery if any host from the above call are new or not existing anymore.
 4. Only if there is not a match the file-based discovery file will be updated
 5. If the file is updated, Prometheus will reload the files configuration.

# Running 
	python -m monitor_promdiscovery -f ./config.yml
	
# Installing
1. Check out the git repo.
2. Install dependency
    
    `pip install -r requirements.txt`
     
3. Build a distribution 

    `python setup.py sdist`

4. Install locally
 
    `pip install dist/monitor-promdiscovery-X.Y.Z.tar.gz`
     
5. Run

    `python -m monitor_promdiscovery -f some_config.yml`




# Configuration
The *monitor-promdiscovery* configuration file should be self explained:
```yaml

op5monitor:  
  url: https://monitor.local  
  user: monitor  
  passwd: monitor  
  # The hostgroup used to select hosts as targets  
  hostgroup: prometheus  
  
prometheus:  
  # path where to create the file-based discovery file  
  sd_file: <sd_directory>/monitor_sd.yml  
  # Additional labels to tag metrics with  
  labels:  
    source: monitor  
    env: prod

logger:
  # Path and name for the log file. If not set sent to stdout
  logfile: monitor-promdiscovery.log
  # Format if day will have current day as post fix
  # format: day
  # Log level
  #level: INFO

``` 

## Promethues configuration
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

# System requirement
Python 3.6

For required packages please review `requirements.txt`


