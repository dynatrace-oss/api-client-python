from dynatrace import Dynatrace
from dynatrace.environment_v2.service_level_objectives import Slo, SloStatus, SloError, SloEvaluationType
from dynatrace.pagination import PaginatedList

SLO_ID = "d4adc421-245e-3bc5-a683-df2ed030997c"


def test_list(dt: Dynatrace):
    slos = dt.slos.list(page_size=20, evaluate=True)

    assert isinstance(slos, PaginatedList)
    assert len(list(slos)) == 2
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
    assert slo.name == "MySLOService"
    assert slo.custom_description == "Service Errors Fivexx SuccessCount / Service RequestCount Total"
    assert slo.evaluated_percentage == 99.92798959015639
    assert slo.error_budget == -0.022010409843616685
    assert slo.status == SloStatus.FAILURE
    assert slo.error == SloError.NONE
    assert slo.use_rate_metric == False
    assert slo.metric_rate == ""
    assert slo.metric_numerator == "builtin:service.errors.fivexx.successCount:splitBy()"
    assert slo.metric_denominator == "builtin:service.requestCount.total:splitBy()"
    assert slo.numerator_value == 1704081
    assert slo.denominator_value == 1705309
    assert slo.target == 99.95
    assert slo.warning == 99.97
    assert slo.evaluation_type == SloEvaluationType.AGGREGATE
    assert slo.timeframe == "-2h"
    assert slo.filter == "type(SERVICE),entityId(SERVICE-D89AF859A68D9072)"
    assert slo.related_open_problems == 0
