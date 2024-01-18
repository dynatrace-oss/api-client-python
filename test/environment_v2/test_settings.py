from datetime import datetime

from dynatrace.environment_v2.settings import SettingsObject, SettingsObjectCreate, SchemaStub
from dynatrace import Dynatrace
from dynatrace.pagination import PaginatedList

settings_dict = {
        "enabled": True,
        "summary": "DT API TEST 22",
        "queryDefinition": {
            "type": "METRIC_KEY",
            "metricKey": "netapp.ontap.node.fru.state",
            "aggregation": "AVG",
            "entityFilter": {
                "dimensionKey": "dt.entity.netapp_ontap:fru",
                "conditions": [],
            },
            "dimensionFilter": [],
        },
        "modelProperties": {
            "type": "STATIC_THRESHOLD",
            "threshold": 100.0,
            "alertOnNoData": False,
            "alertCondition": "BELOW",
            "violatingSamples": 3,
            "samples": 5,
            "dealertingSamples": 5,
        },
        "eventTemplate": {
            "title": "OnTap {dims:type} {dims:fru_id} is in Error State",
            "description": "OnTap field replaceable unit (FRU) {dims:type} with id {dims:fru_id} on node {dims:node} in cluster {dims:cluster} is in an error state.\n",
            "eventType": "RESOURCE",
            "davisMerge": True,
            "metadata": [],
        },
        "eventEntityDimensionKey": "dt.entity.netapp_ontap:fru",
    }
settings_object = SettingsObjectCreate("builtin:anomaly-detection.metric-events", settings_dict, "environment")
test_object_id = "vu9U3hXa3q0AAAABACdidWlsdGluOmFub21hbHktZGV0ZWN0aW9uLm1ldHJpYy1ldmVudHMABnRlbmFudAAGdGVuYW50ACRiYmYzZWNhNy0zMmZmLTM2ZTEtOTFiOS05Y2QxZjE3OTc0YjC-71TeFdrerQ"

def test_list_schemas(dt: Dynatrace):
    schemas = dt.settings.list_schemas()
    assert isinstance(schemas, PaginatedList)
    assert len(list(schemas)) == 3
    assert all(isinstance(s, SchemaStub) for s in schemas)

def test_list_objects(dt: Dynatrace):
    settings = dt.settings.list_objects(schema_id="builtin:anomaly-detection.metric-events")
    assert isinstance(settings, PaginatedList)
    assert len(list(settings)) == 2
    assert all(isinstance(s, SettingsObject) for s in settings)

def test_get_object(dt: Dynatrace):
    setting = dt.settings.get_object(object_id=test_object_id)
    assert isinstance(setting, SettingsObject)
    assert setting.schema_version == "1.0.16"

def test_post_object(dt: Dynatrace):
    response = dt.settings.create_object(body=settings_object)
    assert response[0].get("code") == 200

def test_put_object(dt: Dynatrace):
    response = dt.settings.update_object(test_object_id, settings_object)
    print(response)
    