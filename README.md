# dt-api

**dtapi** is a Python client for the [Dynatrace Rest API].   
It focuses on ease of use and nice type hints, perfect to explore the API and create quick scripts

[Dynatrace Rest API]: https://www.dynatrace.com/support/help/dynatrace-api

## Install

```bash
$ pip install dtapi
```
## Simple Demo

```python
from dynatrace import Dynatrace
from dynatrace import TOO_MANY_REQUESTS_WAIT
from dynatrace.environment_v2.tokens_api import SCOPE_METRICS_READ, SCOPE_METRICS_INGEST

from datetime import datetime, timedelta

# Create a Dynatrace client
dt = Dynatrace("environment_url", "api_token")

# Create a client that handles too many requests (429)
# dt = Dynatrace("environment_url", "api_token", too_many_requests_strategy=TOO_MANY_REQUESTS_WAIT )

# Create a client that automatically retries on errors, up to 5 times, with a 1 second delay between retries
# dt = Dynatrace("environment_url", "api_token", retries=5, retry_delay_ms=1000 )


# Get all hosts and some properties
for entity in dt.entities.list('type("HOST")', fields="properties.memoryTotal,properties.monitoringMode"):
    print(entity.entity_id, entity.display_name, entity.properties)

# Get idle CPU for all hosts
for metric in dt.metrics.query("builtin:host.cpu.idle", resolution="Inf"):
    print(metric)

# Print dimensions, timestamp and values for the AWS Billing Metric
for metric in dt.metrics.query("ext:cloud.aws.billing.estimatedChargesByRegionCurrency"):
    for data in metric.data:
        for timestamp, value in zip(data.timestamps, data.values):
            print(data.dimensions, timestamp, value)

# Get all ActiveGates
for ag in dt.activegates.list():
    print(ag)

# Get metric descriptions for all host metrics
for m in dt.metrics.list("builtin:host.*"):
    print(m)

# Delete endpoints that contain the word test
for plugin in dt.plugins.list():

    # This could also be dt.get_endpoints(plugin.id)
    for endpoint in plugin.endpoints:
        if "test" in endpoint.name:
            endpoint.delete(plugin.id)

# Prints dashboard ID, owner and number of tiles
for dashboard in dt.dashboards.list():
    full_dashboard = dashboard.get_full_dashboard()
    print(full_dashboard.id, dashboard.owner, len(full_dashboard.tiles))

# Delete API Tokens that haven't been used for more than 3 months
for token in dt.tokens.list(fields="+lastUsedDate,+scopes"):
    if token.last_used_date and token.last_used_date < datetime.now() - timedelta(days=90):
        print(f"Deleting token! {token}, last used date: {token.last_used_date}")

# Create an API Token that can read and ingest metrics
new_token = dt.tokens.create("metrics_token", scopes=[SCOPE_METRICS_READ, SCOPE_METRICS_INGEST])
print(new_token.token)
```

## Implementation Progress

### Environment API V2

API                                      |  Level               |  Access                                     |
:-------------                           |  :-------------:     |  :-----                                     |
Access Tokens - API tokens               |  :heavy_check_mark:  |  `dt.tokens`                                |
Access tokens - Tenant tokens            |  :heavy_check_mark:  |  `dt.tenant_tokens`                         |
ActiveGates                              |  :heavy_check_mark:  |  `dt.activegates`                           |
ActiveGates - Auto-update configuration  |  :heavy_check_mark:  |  `dt.activegates_autoupdate_configuration`  |
ActiveGates - Auto-update jobs           |  :heavy_check_mark:  |  `dt.activegates_autoupdate_jobs`           |
Audit Logs                               |  :heavy_check_mark:  |  `dt.audit_logs`                            |
Extensions 2.0                           |  :x:                 |                                             |
Metrics                                  |  :heavy_check_mark:  |  `dt.metrics`                               |
Monitored entities                       |  :warning:           |  `dt.entities`                              |
Monitored entities - Custom tags         |  :x:                 |                                             |
Network zones                            |  :x:                 |                                             |
Problems                                 |  :x:                 |                                             |
Security problems                        |  :x:                 |                                             |
Service-level objectives                 |  :x:                 |                                             

### Environment API V1

API                                    |  Level               | Access                              |
:-------------                         |  :-------------:     | :-----                              |
Anonymization                          |  :x:                 |                                     |
Cluster time                           |  :heavy_check_mark:  |  `dt.time`                          |
Cluster version                        |  :x:                 |                                     |
Deployment                             |  :x:                 |                                     |
Events                                 |  :warning:           |  `dt.events`                        |
JavaScript tag management              |  :x:                 |                                     |
Log monitoring - Custom devices        |  :x:                 |                                     |
Log monitoring - Hosts                 |  :x:                 |                                     |
Log monitoring - Process groups        |  :x:                 |                                     |
Maintenance window                     |  :x:                 |                                     |
OneAgent on a host                     |  :x:                 |                                     |
Problem                                |  :x:                 |                                     |
Synthetic - Locations and nodes        |  :x:                 |                                     |
Synthetic - Monitors                   |  :warning:           |  `dt.synthetic_monitors`                                  |
Synthetic - Third party                |  :heavy_check_mark:  |  `dt.third_part_synthetic_tests`    |
Threshold                              |  :x:                 |                                     |
Timeseries                             |  :warning:           |  `dt.timeseries`                    |
Tokens                                 |  :x:                 |                                     |
Topology & Smartscape - Application    |  :x:                 |                                     |
Topology & Smartscape - Custom device  |  :warning:           |  `dt.custom_devices`                |
Topology & Smartscape - Host           |  :x:                 |                                     |
Topology & Smartscape - Process        |  :x:                 |                                     |
Topology & Smartscape - Process group  |  :x:                 |                                     |
Topology & Smartscape - Service        |  :x:                 |                                     |
User sessions                          |  :x:                 |                                     |


### Configuration API V1

API                                                  |  Level               |  Access                |
:-------------                                       |  :-------------:     |  :-----                |
Alerting Profiles                                    |  :x:                 |                        |
Anomaly detection - Applications                     |  :x:                 |                        |
Anomaly detection - AWS                              |  :x:                 |                        |
Anomaly detection - Database services                |  :x:                 |                        |
Anomaly detection - Disk events                      |  :x:                 |                        |
Anomaly detection - Hosts                            |  :x:                 |                        |
Anomaly detection - Metric events                    |  :x:                 |                        |
Anomaly detection - Process groups                   |  :x:                 |                        |
Anomaly detection - Services                         |  :x:                 |                        |
Anomaly detection - VMware                           |  :x:                 |                        |
Automatically applied tags                           |  :x:                 |                        |
AWS credentials configuration                        |  :x:                 |                        |
AWS PrivateLink                                      |  :x:                 |                        |
Azure credentials configuration                      |  :x:                 |                        |
Calculated metrics - Log monitoring                  |  :x:                 |                        |
Calculated metrics - Mobile & custom applications    |  :x:                 |                        |
Calculated metrics - Services                        |  :x:                 |                        |
Calculated metrics - Synthetic                       |  :x:                 |                        |
Calculated metrics - Web applications                |  :x:                 |                        |
Cloud Foundry credentials configuration              |  :x:                 |                        |
Conditional naming                                   |  :x:                 |                        |
Credential vault                                     |  :x:                 |                        |
Dashboards                                           |  :warning:           |  `dt.dashboards`       |
Data privacy and security                            |  :x:                 |                        |
Extensions                                           |  :heavy_check_mark:  |  `dt.extensions`       |
Frequent issue detection                             |  :x:                 |                        |
Kubernetes credentials configuration                 |  :x:                 |                        |
Maintenance windows                                  |  :x:                 |                        |
Management zones                                     |  :warning:           |                        |
Notifications                                        |  :warning:           |  `dt.notifications`    |
OneAgent - Environment-wide configuration            |  :x:                 |                        |
OneAgent in a host group                             |  :x:                 |                        |
OneAgent on a host                                   |  :x:                 |                        |
Plugins                                              |  :warning:           |  `dt.plugins`          |
Remote environments                                  |  :x:                 |                        |
Reports                                              |  :x:                 |                        |
RUM - Allowed beacon origins for CORS                |  :x:                 |                        |
RUM - Application detection rules                    |  :x:                 |                        |
RUM - Application detection rules - Host detection   |  :x:                 |                        |
RUM - Content resources                              |  :x:                 |                        |
RUM - Geographic regions - custom client IP headers  |  :x:                 |                        |
RUM - Geographic regions - IP address mapping        |  :x:                 |                        |
RUM - Mobile and custom application configuration    |  :x:                 |                        |
RUM - Web application configuration                  |  :x:                 |                        |
Service - Custom services                            |  :x:                 |                        |
Service - Detection full web request                 |  :x:                 |                        |
Service - Detection full web service                 |  :x:                 |                        |
Service - Detection opaque and external web request  |  :x:                 |                        |
Service - Detection opaque and external web service  |  :x:                 |                        |
Service - Failure detection parameter sets           |  :x:                 |                        |
Service - Failure detection rules                    |  :x:                 |                        |
Service - IBM MQ tracing                             |  :x:                 |                        |
Service - Request attributes                         |  :x:                 |                        |
Service - Request naming                             |  :x:                 |                        |
