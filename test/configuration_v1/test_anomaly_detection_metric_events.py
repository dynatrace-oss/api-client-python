from dynatrace import Dynatrace
from dynatrace.configuration_v1.metric_events import (
    AggregationType,
    DisabledReason,
    MetricEventAlertingScopeFilterType,
    MetricEventAlertingScope,
    MetricEventAutoAdaptiveBaselineMonitoringStrategy,
    MetricEventDimension,
    MetricEventDimensionsFilterType,
    MetricEventMonitoringStrategyType,
    MetricEventShortRepresentation,
    MetricEventStaticThresholdMonitoringStrategy,
    Severity,
    WarningReason,
    Unit,
)
from dynatrace.pagination import PaginatedList

from typing import List

STATIC_ID = "ruxit.python.rabbitmq:node_status:node_failed"
STATIC_NAME = "RabbitMQ Node failed"
BASELINE_ID = "d3baaaed-3441-4931-bf24-25c4e12e137f"
BASELINE_NAME = "Mint alert for static"


def test_list(dt: Dynatrace):
    metric_events = dt.anomaly_detection_metric_events.list()
    assert isinstance(metric_events, PaginatedList)

    list_metric_events = list(metric_events)
    assert len(list_metric_events) == 193

    first = list_metric_events[0]
    assert isinstance(first, MetricEventShortRepresentation)

    assert first.id == STATIC_ID
    assert first.name == STATIC_NAME


def test_get_full_configuration(dt: Dynatrace):
    metric_events = dt.anomaly_detection_metric_events.list()
    list_metric_events = list(metric_events)

    for metric_event in list_metric_events:
        if metric_event.id == STATIC_ID:
            # static
            full = metric_event.get_full_metric_event()

            # type checks
            assert isinstance(full.name, str)
            assert isinstance(full.metric_id, str)
            assert isinstance(full.severity, Severity)
            assert isinstance(full.enabled, bool)
            assert isinstance(full.disabled_reason, DisabledReason)
            assert isinstance(full.aggregation_type, AggregationType)
            assert isinstance(full.warning_reason, WarningReason)
            assert isinstance(full.alerting_scope, List)
            assert isinstance(full.monitoring_strategy, MetricEventStaticThresholdMonitoringStrategy)
            assert isinstance(full.metric_dimensions, List)
            assert isinstance(full.primary_dimension_key, type(None))

            # value checks
            assert full.name == STATIC_NAME
            assert full.id == STATIC_ID
            assert full.aggregation_type == AggregationType.VALUE
            assert full.severity == Severity.AVAILABILITY
            assert full.enabled == True
            assert full.disabled_reason == DisabledReason.NONE
            assert full.monitoring_strategy.type == MetricEventMonitoringStrategyType.STATIC_THRESHOLD
            assert full.monitoring_strategy.unit == Unit.COUNT
            assert full.monitoring_strategy.violating_samples == 3
            assert full.metric_dimensions[0].filter_type == MetricEventDimensionsFilterType.STRING

        elif metric_event.id == BASELINE_ID:
            # static
            full = metric_event.get_full_metric_event()

            # type checks
            assert isinstance(full.monitoring_strategy, MetricEventAutoAdaptiveBaselineMonitoringStrategy)

            # value checks
            assert full.monitoring_strategy.type == MetricEventMonitoringStrategyType.AUTO_ADAPTIVE_BASELINE

            break

        else:
            continue
