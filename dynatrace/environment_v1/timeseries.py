from enum import Enum
from typing import Optional, List, Union

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient


class Unit(Enum):
    BIT = "Bit(bit)"
    BITPERHOUR = "BitPerHour(bit/h)"
    BITPERMINUTE = "BitPerMinute(bit/min)"
    BITPERSECOND = "BitPerSecond(bit/s)"
    BYTE = "Byte(B)"
    BYTEPERHOUR = "BytePerHour(B/h)"
    BYTEPERMINUTE = "BytePerMinute(B/min)"
    BYTEPERSECOND = "BytePerSecond(B/s)"
    CORES = "Cores"
    COUNT = "Count(count)"
    DAY = "Day(ds)"
    DECIBELMILLIWATT = "DecibelMilliWatt(dBm)"
    G = "G"
    GIBIBYTE = "GibiByte(GiB)"
    GIGABYTE = "GigaByte(GB)"
    HOUR = "Hour(hs)"
    KIBIBYTE = "KibiByte(KiB)"
    KIBIBYTEPERHOUR = "KibiBytePerHour(KiB/h)"
    KIBIBYTEPERMINUTE = "KibiBytePerMinute(KiB/min)"
    KIBIBYTEPERSECOND = "KibiBytePerSecond(KiB/s)"
    KILOBYTE = "KiloByte(kB)"
    KILOBYTEPERHOUR = "KiloBytePerHour(kB/h)"
    KILOBYTEPERMINUTE = "KiloBytePerMinute(kB/min)"
    KILOBYTEPERSECOND = "KiloBytePerSecond(kB/s)"
    M = "M"
    MEBIBYTE = "MebiByte(MiB)"
    MEBIBYTEPERHOUR = "MebiBytePerHour(MiB/h)"
    MEBIBYTEPERMINUTE = "MebiBytePerMinute(MiB/min)"
    MEBIBYTEPERSECOND = "MebiBytePerSecond(MiB/s)"
    MEGABYTE = "MegaByte(MB)"
    MEGABYTEPERHOUR = "MegaBytePerHour(MB/h)"
    MEGABYTEPERMINUTE = "MegaBytePerMinute(MB/min)"
    MEGABYTEPERSECOND = "MegaBytePerSecond(MB/s)"
    MICROSECOND = "MicroSecond(µs)"
    MILLISECOND = "MilliSecond(ms)"
    MILLISECONDPERMINUTE = "MilliSecondPerMinute(ms/min)"
    MINUTE = "Minute(mins)"
    MONTH = "Month(mos)"
    NOT_APPLICABLE = "N/A"
    NANOSECOND = "NanoSecond(ns)"
    NANOSECONDPERMINUTE = "NanoSecondPerMinute(ns/min)"
    PERHOUR = "PerHour(count/h)"
    PERMINUTE = "PerMinute(count/min)"
    PERSECOND = "PerSecond(count/s)"
    PERCENT = "Percent(%)"
    PIXEL = "Pixel(px)"
    PROMILLE = "Promille(‰)"
    RATIO = "Ratio"
    SECOND = "Second(s)"
    STATE = "State"
    UNSPECIFIED = "Unspecified"
    WEEK = "Week(ws)"
    YEAR = "Year(ys)"
    K = "k"
    M_CORES = "mCores"


class TimeSerieService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def create_timeseries(
        self,
        metric_id: str,
        display_name: Optional[str],
        unit: Optional[Union[Unit, str]] = None,
        dimensions: Optional[List[str]] = None,
        technologies: Optional[List[str]] = None,
    ) -> "TimeseriesRegistrationMessage":

        unit: Unit = Unit(unit)
        return TimeseriesRegistrationMessage(
            self.__http_client,
            metric_id=metric_id,
            display_name=display_name,
            unit=unit.value,
            dimensions=dimensions,
            technologies=technologies,
        )


class TimeseriesRegistrationMessage(DynatraceObject):
    def __init__(
        self,
        http_client,
        metric_id: str,
        display_name: Optional[str],
        unit: Optional[str] = None,
        dimensions: Optional[List[str]] = None,
        technologies: Optional[List[str]] = None,
    ):
        self.metric_id = metric_id

        raw_element = {
            "displayName": display_name,
            "unit": unit,
            "dimensions": dimensions,
            "types": technologies,
        }
        super().__init__(http_client, None, raw_element)

    def put(self):
        return self._http_client.make_request(f"/api/v1/timeseries/{self.metric_id}", params=self._raw_element, method="PUT")
