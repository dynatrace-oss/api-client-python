from datetime import datetime
from typing import Optional, List, Dict, Tuple


from dynatrace.dynatrace_object import DynatraceObject


class CustomDevicePushMessage(DynatraceObject):
    def __init__(
        self,
        http_client,
        device_id: str,
        display_name: Optional[str] = None,
        group: Optional[str] = None,
        ip_addresses: Optional[List[str]] = None,
        listen_ports: Optional[List[int]] = None,
        technology: Optional[str] = None,
        favicon: Optional[str] = None,
        config_url: Optional[str] = None,
        properties: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        series: Optional[List] = None,
        host_names: Optional[List[str]] = None,
    ):
        self.device_id = device_id
        self.display_name: Optional[str] = display_name
        self.group: Optional[str] = group
        self.ip_addresses: Optional[List[str]] = ip_addresses
        self.listen_ports: Optional[List[int]] = listen_ports
        self.technology: Optional[str] = technology
        self.favicon: Optional[str] = favicon
        self.config_url: Optional[str] = config_url
        self.properties: Optional[Dict[str, str]] = properties
        self.tags: Optional[List[str]] = tags
        self.__series: List["EntityTimeseriesData"] = series
        if self.__series is None:
            self.__series: List["EntityTimeseriesData"] = []
        self.host_names: Optional[List[str]] = host_names

        raw_element = {
            "displayName": self.display_name,
            "group": self.group,
            "ipAddresses": self.ip_addresses,
            "listenPorts": self.listen_ports,
            "type": self.technology,
            "favicon": self.favicon,
            "configUrl": self.config_url,
            "properties": self.properties,
            "tags": self.tags,
            "series": [s._raw_element for s in self.__series] if self.__series else None,
            "hostNames": self.host_names,
        }
        super().__init__(http_client, None, raw_element)

    @property
    def series(self) -> List["EntityTimeseriesData"]:
        return self.__series

    @series.setter
    def series(self, series: List["EntityTimeseriesData"]):
        self.__series = series
        self._raw_element["series"] = [s._raw_element for s in self.__series]

    def post(self, only_valid_data_points=False):
        try:
            response = self._http_client.make_request(
                f"/api/v1/entity/infrastructure/custom/{self.device_id}", params=self._raw_element, method="POST"
            )
            return response
        except Exception as e:
            if only_valid_data_points and "configuration.Creation timestamp is:" in f"{e}":
                max_timestamp = int(f"{e}".split("configuration.Creation timestamp is:")[1].split('"')[0].strip())
                max_timestamp = datetime.fromtimestamp(max_timestamp / 1000)
                self._http_client.log.warning(f"Some data points were invalid, removing data points older than {max_timestamp}")
                for s in self.series:
                    s.data_points = [d for d in s.data_points if d.timestamp >= max_timestamp]
                self._raw_element["series"] = [s._raw_element for s in self.series]
                return self.post()
            else:
                raise e

    def absolute(self, key: str, value: float, timestamp: Optional[datetime] = None, dimensions: Optional[Dict[str, str]] = None):
        data_point = DataPoint(value, timestamp)
        self.series.append(EntityTimeseriesData(self._http_client, key, [data_point], dimensions))
        self.series = self.series  # Ugly as hell hack because of setter, and I don't want to subclass list


class EntityTimeseriesData(DynatraceObject):
    def __init__(
        self, http_client, timeseries_id: str, data_points: List["DataPoint"], dimensions: Optional[Dict[str, str]] = None
    ):
        self.timeseries_id: str = timeseries_id
        self.__data_points: List["DataPoint"] = data_points
        raw_element = {
            "timeseriesId": timeseries_id,
            "dimensions": dimensions,
            "dataPoints": [[int(data_point.timestamp.timestamp() * 1000), data_point.value] for data_point in data_points],
        }
        super().__init__(http_client, None, raw_element)

    def __repr__(self):
        return f"Series(id={self.timeseries_id}, data_points={self.data_points})"

    @property
    def data_points(self) -> List["DataPoint"]:
        return self.__data_points

    @data_points.setter
    def data_points(self, data_points: List["DataPoint"]):
        self.__data_points = data_points
        self._raw_element["dataPoints"] = [
            [int(data_point.timestamp.timestamp() * 1000), data_point.value] for data_point in self.__data_points
        ]


class DataPoint:
    def __init__(self, value: float, timestamp: Optional[datetime] = None):
        self.timestamp = timestamp
        if self.timestamp is None:
            self.timestamp = datetime.now()
        self.value = value

    def __repr__(self):
        return f"[{self.timestamp}, {self.value}]"
