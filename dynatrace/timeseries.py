from typing import Optional, List

from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.http_client import HttpClient

UNIT_BIT = "Bit(bit)"
UNIT_BITPERHOUR = "BitPerHour(bit/h)"
UNIT_BITPERMINUTE = "BitPerMinute(bit/min)"
UNIT_BITPERSECOND = "BitPerSecond(bit/s)"
UNIT_BYTE = "Byte(B)"
UNIT_BYTEPERHOUR = "BytePerHour(B/h)"
UNIT_BYTEPERMINUTE = "BytePerMinute(B/min)"
UNIT_BYTEPERSECOND = "BytePerSecond(B/s)"
UNIT_CORES = "Cores"
UNIT_COUNT = "Count(count)"
UNIT_DAY = "Day(ds)"
UNIT_DECIBELMILLIWATT = "DecibelMilliWatt(dBm)"
UNIT_G = "G"
UNIT_GIBIBYTE = "GibiByte(GiB)"
UNIT_GIGABYTE = "GigaByte(GB)"
UNIT_HOUR = "Hour(hs)"
UNIT_KIBIBYTE = "KibiByte(KiB)"
UNIT_KIBIBYTEPERHOUR = "KibiBytePerHour(KiB/h)"
UNIT_KIBIBYTEPERMINUTE = "KibiBytePerMinute(KiB/min)"
UNIT_KIBIBYTEPERSECOND = "KibiBytePerSecond(KiB/s)"
UNIT_KILOBYTE = "KiloByte(kB)"
UNIT_KILOBYTEPERHOUR = "KiloBytePerHour(kB/h)"
UNIT_KILOBYTEPERMINUTE = "KiloBytePerMinute(kB/min)"
UNIT_KILOBYTEPERSECOND = "KiloBytePerSecond(kB/s)"
UNIT_M = "M"
UNIT_MEBIBYTE = "MebiByte(MiB)"
UNIT_MEBIBYTEPERHOUR = "MebiBytePerHour(MiB/h)"
UNIT_MEBIBYTEPERMINUTE = "MebiBytePerMinute(MiB/min)"
UNIT_MEBIBYTEPERSECOND = "MebiBytePerSecond(MiB/s)"
UNIT_MEGABYTE = "MegaByte(MB)"
UNIT_MEGABYTEPERHOUR = "MegaBytePerHour(MB/h)"
UNIT_MEGABYTEPERMINUTE = "MegaBytePerMinute(MB/min)"
UNIT_MEGABYTEPERSECOND = "MegaBytePerSecond(MB/s)"
UNIT_MICROSECOND = "MicroSecond(µs)"
UNIT_MILLISECOND = "MilliSecond(ms)"
UNIT_MILLISECONDPERMINUTE = "MilliSecondPerMinute(ms/min)"
UNIT_MINUTE = "Minute(mins)"
UNIT_MONTH = "Month(mos)"
UNIT_NOT_APPLICABLE = "N/A"
UNIT_NANOSECOND = "NanoSecond(ns)"
UNIT_NANOSECONDPERMINUTE = "NanoSecondPerMinute(ns/min)"
UNIT_PERHOUR = "PerHour(count/h)"
UNIT_PERMINUTE = "PerMinute(count/min)"
UNIT_PERSECOND = "PerSecond(count/s)"
UNIT_PERCENT = "Percent(%)"
UNIT_PIXEL = "Pixel(px)"
UNIT_PROMILLE = "Promille(‰)"
UNIT_RATIO = "Ratio"
UNIT_SECOND = "Second(s)"
UNIT_STATE = "State"
UNIT_UNSPECIFIED = "Unspecified"
UNIT_WEEK = "Week(ws)"
UNIT_YEAR = "Year(ys)"
UNIT_K = "k"
UNIT_M_CORES = "mCores"


class TimeSerieService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def create_timeseries(
        self,
        metric_id: str,
        display_name: Optional[str],
        unit: Optional[str] = None,
        dimensions: Optional[List[str]] = None,
        technologies: Optional[List[str]] = None,
    ) -> "TimeseriesRegistrationMessage":

        return TimeseriesRegistrationMessage(
            self.__http_client,
            metric_id=metric_id,
            display_name=display_name,
            unit=unit,
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
