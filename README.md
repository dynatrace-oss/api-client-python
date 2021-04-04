from dynatrace.token import SCOPE_METRICS_READ# dt-api

dtapi is a Python library to access the [Dynatrace Rest API]

[Dynatrace Rest API]: https://www.dynatrace.com/support/help/dynatrace-api

## Install

```bash
$ pip install dtapi
```

## Simple Demo

```python
from datetime import datetime, timedelta

from dynatrace import Dynatrace
from dynatrace import TOO_MANY_REQUESTS_WAIT
from dynatrace.environment_v2.token import SCOPE_METRICS_READ, SCOPE_METRICS_INGEST

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
    if token.last_used_date < datetime.now() - timedelta(days=90):
        print(f"Deleting token! {token}, last used date: {token.last_used_date}")

# Create an API Token that can read and ingest metrics
new_token = dt.tokens.create("metrics_token", scopes=[SCOPE_METRICS_READ, SCOPE_METRICS_INGEST])
print(new_token.token)
```

## Implementation Progress

Spec                | API                                       | Level              | Access  |
:-------------      | :-------------                            |:-------------:     | :-----  |
Environment API v2  | Access Tokens - API tokens                | :heavy_check_mark: | `dt.tokens`   |
Environment API v2  | Access tokens - Tenant tokens             | :x:                |     |
Environment API v2  | ActiveGates                               | :heavy_check_mark: | `dt.activegates`    |
Environment API v2  | ActiveGates - Auto-update configuration   | :warning:          | `dt.activegates_autoupdate`    |
Environment API v2  | ActiveGates - Auto-update jobs            | :x:                |     |
Environment API v2  | Audit Logs                                | :x:                |      |
Environment API v2  | Extensions 2.0                            | :warning:          | `dt.extensions`     |
Environment API v2  | Metrics                                   | :warning:          | `dt.metrics`     |
Environment API v2  | Monitored entities                        | :warning:          | `dt.entities`     |
Environment API v2  | Monitored entities - Custom tags          | :x:                |     |
Environment API v2  | Network zones                             | :x:                |     |
Environment API v2  | Problems                                  | :x:                |     |
Environment API v2  | Security problems                         | :x:                |     |
Environment API v2  | Service-level objectives                  | :x:                |     |
