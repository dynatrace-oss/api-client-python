"""
Copyright 2021 Dynatrace LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from enum import Enum
from typing import Dict, Any, Optional

from dynatrace.http_client import HttpClient
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.pagination import PaginatedList


class SloService:
    ENDPOINT = "/api/v2/slo"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        page_size: Optional[int] = 10,
        time_from: Optional[str] = "now-2w",
        time_to: Optional[str] = None,
        slo_selector: Optional[str] = None,
        sort: Optional[str] = "name",
        time_frame: Optional[str] = "CURRENT",
        page_idx: Optional[int] = 1,
        demo: Optional[bool] = False,
        evaluate: Optional[bool] = False,
    ) -> PaginatedList["Slo"]:
        """Lists all available SLOs along with calculated values

        :return: list of SLOs
        """

    def get(self, slo_id: str):
        """Gets parameters and the calculated value of an SLO

        :param slo_id: the ID of the SLO
        :return: the SLO and its details
        """
        pass

    def create(self):
        """Creates a new SLO"""
        pass

    def update(self):
        pass

    def delete(self):
        pass


class Slo(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        # required
        self.name: str = raw_element.get("name")
        self.id: str = raw_element.get("id")
        self.target: float = raw_element.get("target")
        self.timeframe: str = raw_element.get("timeframe")
        self.status: SloStatus = SloStatus(raw_element.get("status"))
        self.metric_rate: str = raw_element.get("metricRate")
        self.metric_numerator: str = raw_element.get("metricNumerator")
        self.metric_denominator: str = raw_element.get("metricDenominator")
        self.evaluation_type: SloEvaluationType = SloEvaluationType(raw_element.get("evaluationType"))

        # optional
        self.error_budget: Optional[float] = raw_element.get("errorBudget", 0)
        self.numerator_value: Optional[float] = raw_element.get("numeratorValue", 0)
        self.denominator_value: Optional[float] = raw_element.get("denominatorValue", 0)
        self.related_open_problems: Optional[int] = raw_element.get("relatedOpenProblems", 0)
        self.use_rate_metric: Optional[bool] = raw_element.get("useRateMetric", False)
        self.evaluated_percentage: Optional[float] = raw_element.get("evaluatedPercentage", 0)
        self.filter: Optional[str] = raw_element.get("filter")
        self.enabled: Optional[bool] = raw_element.get("enabled", False)
        self.description: Optional[str] = raw_element.get("description")
        self.error: Optional[SloError] = raw_element.get("error", SloError.NONE)


class SloEvaluationType(Enum):
    AGGREGATE = "AGGREGATE"


class SloStatus(Enum):
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"


class SloError(Enum):
    DIFFERENT_ENTITY_TYPE_IN_METRICS = "DIFFERENT_ENTITY_TYPE_IN_METRICS"
    EVALUATION_TIMEFRAME_OUT_OF_BOUNDS = "EVALUATION_TIMEFRAME_OUT_OF_BOUNDS"
    FILTER_MATCHES_IN_CONDITION_LIMIT_EXCEEDED = "FILTER_MATCHES_IN_CONDITION_LIMIT_EXCEEDED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    INVALID_ENTITY_SELECTOR = "INVALID_ENTITY_SELECTOR"
    INVALID_METRIC_DENOMINATOR = "INVALID_METRIC_DENOMINATOR"
    INVALID_METRIC_NUMERATOR = "INVALID_METRIC_NUMERATOR"
    INVALID_METRIC_SELECTOR = "INVALID_METRIC_SELECTOR"
    INVALID_TIMEFRAME = "INVALID_TIMEFRAME"
    METRICS_NOT_RESOLVED = "METRICS_NOT_RESOLVED"
    METRICS_NO_DATA = "METRICS_NO_DATA"
    METRIC_DENOMINATOR_NOT_RESOLVED = "METRIC_DENOMINATOR_NOT_RESOLVED"
    METRIC_DENOMINATOR_NO_DATA = "METRIC_DENOMINATOR_NO_DATA"
    METRIC_DENOMINATOR_NO_DATA_POINTS = "METRIC_DENOMINATOR_NO_DATA_POINTS"
    METRIC_DENOMINATOR_ZERO = "METRIC_DENOMINATOR_ZERO"
    METRIC_EXPRESSION_NOT_RESOLVED = "METRIC_EXPRESSION_NOT_RESOLVED"
    METRIC_EXPRESSION_NO_DATA = "METRIC_EXPRESSION_NO_DATA"
    METRIC_EXPRESSION_NO_DATA_POINTS = "METRIC_EXPRESSION_NO_DATA_POINTS"
    METRIC_GENERIC_TSM_FAULT = "METRIC_GENERIC_TSM_FAULT"
    METRIC_NUMERATOR_NOT_RESOLVED = "METRIC_NUMERATOR_NOT_RESOLVED"
    METRIC_NUMERATOR_NO_DATA = "METRIC_NUMERATOR_NO_DATA"
    METRIC_NUMERATOR_NO_DATA_POINTS = "METRIC_NUMERATOR_NO_DATA_POINTS"
    METRIC_RATE_NOT_RESOLVED = "METRIC_RATE_NOT_RESOLVED"
    METRIC_RATE_NO_DATA = "METRIC_RATE_NO_DATA"
    METRIC_RATE_NO_DATA_POINTS = "METRIC_RATE_NO_DATA_POINTS"
    METRIC_TOO_MANY_RESULTS = "METRIC_TOO_MANY_RESULTS"
    NONE = "NONE"
