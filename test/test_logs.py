from dynatrace import Dynatrace
from datetime import datetime

from dynatrace.environment_v2.logs import LogRecord, EventType, LogRecordStatus
from dynatrace.pagination import PaginatedList


def test_export(dt: Dynatrace):
    logs = dt.logs.export(time_from="now-10m")
    assert isinstance(logs, PaginatedList)

    logs = list(logs)
    assert len(logs) == 18

    first = logs[0]
    assert isinstance(first, LogRecord)
    assert first.additional_columns['dt.extension.ds'][0] == "python"
    assert first.content.startswith("Failed to assign")
    assert first.event_type == EventType.SFM
    assert first.status == LogRecordStatus.ERROR
    assert first.timestamp == datetime.utcfromtimestamp(1683574915193 / 1000)

