# dt-api

dtapi is a Python library to access the [Dynatrace Rest API]

[Dynatrace Rest API]: https://www.dynatrace.com/support/help/dynatrace-api

## Install

```bash
$ pip install dtapi
```

## Simple Demo

```python
from dynatrace import Dynatrace
from dynatrace.constants import TOO_MANY_REQUESTS_WAIT
    
# Create a Dynatrace client
dt = Dynatrace("environment_url", "api_token" )

# Create a client that handles too many requests (429)
dt = Dynatrace("environment_url", "api_token", too_many_requests_strategy=TOO_MANY_REQUESTS_WAIT )


# Get all hosts and some properties
for entity in dt.get_entities('type("HOST")', fields="properties.memoryTotal,properties.monitoringMode"):
    print(entity.entity_id, entity.display_name, entity.properties)

# Get idle CPU for all hosts
for metric in dt.query_metrics("builtin:host.cpu.idle", page_size=5000, resolution="Inf"):
     print(metric)

# Get all ActiveGates
for ag in dt.get_activegates():
    print(ag)

# Get metric descriptions for all host metrics
for m in dt.get_metrics("builtin:host.*"):
    print(m)

# Delete endpoints that contain the word test
for plugin in dt.get_plugins():
    
    # This could also be dt.get_endpoints(plugin.id)    
    for endpoint in plugin.endpoints:
        if "test" in endpoint.name:
            endpoint.delete(plugin.id)

# Prints dashboard ID, owner and number of tiles
for dashboard in dt.get_dashboards():
    # To get the tiles, we need the full dashboard details
    # This could also be dt.get_dashboard(dashboard.id)    
    full = dashboard.get_full_dashboard()
    print(dashboard.id, dashboard.owner, len(full.tiles))
```