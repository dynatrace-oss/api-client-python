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
    
# Create a Dynatrace client
dt = Dynatrace("environment_url", "api_token" )

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
```