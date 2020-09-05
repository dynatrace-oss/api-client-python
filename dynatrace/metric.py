from typing import List

from dynatrace.metric_series import MetricSeries
from dynatrace.dynatrace_object import DynatraceObject


class Metric(DynatraceObject):
    @property
    def metric_id(self) -> str:
        return self._metric_id

    @property
    def data(self) -> List[MetricSeries]:
        return self._data

    def _create_from_raw_data(self, raw_element: dict):
        self._metric_id = raw_element.get("metricId")
        self._data = [
            MetricSeries(self._http_client, self._headers, metric_serie) for metric_serie in raw_element.get("data", [])
        ]
