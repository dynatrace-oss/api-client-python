from dynatrace import Dynatrace

from dynatrace.environment_v2.metrics import MetricDescriptor, Unit, AggregationType, Transformation, ValueType, MetricSeriesCollection
from dynatrace.pagination import PaginatedList
from dynatrace.utils import int64_to_datetime


def test_list(dt: Dynatrace):
    metrics = dt.metrics.list()
    assert isinstance(metrics, PaginatedList)
    for metric in metrics:
        assert isinstance(metric, MetricDescriptor)
        assert metric.metric_id == "builtin:apps.other.apdex.osAndGeo"
        assert metric.display_name == "Apdex (by OS, geolocation) [mobile, custom]"
        assert metric.description == ""
        assert metric.unit == Unit.NOTAPPLICABLE
        break


def test_list_fields(dt: Dynatrace):
    metrics = dt.metrics.list(
        fields="+tags,+dduBillable,+created,+lastWritten,+aggregationTypes,+defaultAggregation,+dimensionDefinitions,+transformations,+entityType"
    )
    assert isinstance(metrics, PaginatedList)

    for metric in metrics:
        assert isinstance(metric, MetricDescriptor)
        assert metric.metric_id == "builtin:apps.other.apdex.osAndGeo"
        assert metric.display_name == "Apdex (by OS, geolocation) [mobile, custom]"
        assert metric.description == ""
        assert metric.unit == Unit.NOTAPPLICABLE
        assert not metric.ddu_billable
        assert metric.created is None
        assert metric.last_written == int64_to_datetime(1620514220905)
        assert metric.entity_type == ["CUSTOM_APPLICATION", "MOBILE_APPLICATION"]
        assert metric.aggregation_types == [AggregationType.AUTO, AggregationType.AUTO.VALUE]
        assert Transformation.FOLD in metric.transformations
        assert metric.default_aggregation.type == "value"
        assert len(metric.dimension_definitions) == 3
        assert metric.dimension_definitions[0].key == "dt.entity.device_application"
        assert metric.dimension_definitions[0].name == "Application"
        assert metric.dimension_definitions[0].index == 0
        assert metric.dimension_definitions[0].type == "ENTITY"
        break


def test_list_params(dt: Dynatrace):

    written_since = int64_to_datetime(1621029621)

    metrics = dt.metrics.list(
        metric_selector="builtin:host.*",
        written_since=written_since,
        metadata_selector='unit("Percent")',
        fields="+tags,+dduBillable,+created,+lastWritten,+aggregationTypes,+defaultAggregation,+dimensionDefinitions,+transformations,+entityType",
    )

    for metric in metrics:
        assert metric.metric_id == "builtin:host.cpu.idle"
        assert metric.display_name == "CPU idle"
        assert metric.description == ""
        assert metric.unit == Unit.PERCENT
        assert not metric.ddu_billable
        assert metric.last_written == int64_to_datetime(1621030025348)
        assert metric.entity_type == ["HOST"]
        assert metric.default_aggregation.type == "avg"
        assert metric.tags == []
        assert metric.dimension_definitions[0].key == "dt.entity.host"
        break


def test_get(dt: Dynatrace):

    metric = dt.metrics.get("builtin:host.cpu.idle")

    assert metric.metric_id == "builtin:host.cpu.idle"
    assert metric.display_name == "CPU idle"
    assert metric.description == ""
    assert metric.unit == Unit.PERCENT
    assert not metric.ddu_billable
    assert metric.last_written == int64_to_datetime(1621030565348)
    assert metric.entity_type == ["HOST"]
    assert metric.default_aggregation.type == "avg"
    assert metric.tags == []
    assert metric.dimension_definitions[0].key == "dt.entity.host"
    assert metric.metric_value_type.type == ValueType.SCORE


def test_query(dt: Dynatrace):
    time_from = int64_to_datetime(1621020000000)
    time_to = int64_to_datetime(1621025000000)

    results = dt.metrics.query("builtin:host.cpu.idle", time_from=time_from, time_to=time_to)
    assert isinstance(results, PaginatedList)

    first = list(results)[0]

    assert isinstance(first, MetricSeriesCollection)
    assert first.metric_id == "builtin:host.cpu.idle"
    assert len(first.data) == 1

    first_data = first.data[0]
    assert first_data.dimension_map == {"dt.entity.host": "HOST-82F576674F19AC16"}
    assert first_data.dimensions == ["HOST-82F576674F19AC16"]
    assert len(first_data.timestamps) == 84
    assert len(first_data.timestamps) == len(first_data.values)
    assert first_data.timestamps[0] == int64_to_datetime(1621020060000)
    assert first_data.values[0] == 89.91581217447917


def test_ingest(dt: Dynatrace):
    ingest = dt.metrics.ingest(["a 1", "b 2"])
    assert isinstance(ingest, dict)
    assert ingest["linesOk"] == 1
    assert ingest["linesInvalid"] == 0
    assert ingest["error"] is None
