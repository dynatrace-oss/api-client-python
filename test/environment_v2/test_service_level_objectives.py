from dynatrace import Dynatrace
from dynatrace.environment_v2.service_level_objectives import Slo, SloStatus, SloError, SloEvaluationType
from dynatrace.pagination import PaginatedList

SLO_ID = "88991da4-be17-3d57-aada-cfb3977767f4"


def test_list(dt: Dynatrace):
    slos = dt.slos.list(enabled_slos="all")

    assert isinstance(slos, PaginatedList)
    assert len(list(slos)) == 4
    assert all(isinstance(s, Slo) for s in slos)


def test_get(dt: Dynatrace):
    slo = dt.slos.get(slo_id=SLO_ID)

    # type checks
    assert isinstance(slo, Slo)
    assert isinstance(slo.enabled, bool)
    assert isinstance(slo.name, str)
    assert isinstance(slo.custom_description, str)
    assert isinstance(slo.evaluated_percentage, float)
    assert isinstance(slo.error_budget, float)
    assert isinstance(slo.status, SloStatus)
    assert isinstance(slo.error, SloError)
    assert isinstance(slo.use_rate_metric, bool)
    assert isinstance(slo.metric_rate, str)
    assert isinstance(slo.metric_numerator, str)
    assert isinstance(slo.metric_denominator, str)
    assert isinstance(slo.numerator_value, (float, int))
    assert isinstance(slo.denominator_value, (float, int))
    assert isinstance(slo.target, float)
    assert isinstance(slo.warning, float)
    assert isinstance(slo.evaluation_type, SloEvaluationType)
    assert isinstance(slo.timeframe, str)
    assert isinstance(slo.filter, str)
    assert isinstance(slo.related_open_problems, int)

    # value checks
    assert slo.id == SLO_ID
    assert slo.enabled == True
    assert slo.name == "test123"
    assert slo.custom_description == "test"
    assert slo.evaluated_percentage == 100.0
    assert slo.error_budget == 2.0
    assert slo.status == SloStatus.SUCCESS
    assert slo.error == SloError.NONE
    assert slo.metric_rate == ""
    assert slo.metric_numerator == ""
    assert slo.metric_denominator == ""
    assert slo.numerator_value == 0.0
    assert slo.denominator_value == 0.0
    assert slo.target == 98.0
    assert slo.warning == 99.0
    assert slo.evaluation_type == SloEvaluationType.AGGREGATE
    assert slo.timeframe == "now-1h"
    assert slo.filter == ""
    assert slo.related_open_problems == 0
