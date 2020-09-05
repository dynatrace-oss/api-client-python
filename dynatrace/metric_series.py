from datetime import datetime
from typing import List

from dynatrace.dynatrace_object import DynatraceObject


class MetricSeries(DynatraceObject):
    @property
    def timestamps(self) -> List[datetime]:
        return self._timestamps

    @property
    def dimensions(self) -> List[str]:
        return self._dimensions

    @property
    def values(self) -> List[float]:
        return self._values

    def _create_from_raw_data(self, raw_element):
        self._timestamps = [datetime.utcfromtimestamp(timestamp / 1000) for timestamp in raw_element.get("timestamps", [])]
        self._dimensions = raw_element.get("dimensions", [])
        self._values = raw_element.get("values", [])
