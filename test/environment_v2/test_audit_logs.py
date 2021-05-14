from dynatrace import Dynatrace
from datetime import datetime

from dynatrace.environment_v2.audit_logs import AuditLogEntry, EventType, Category, UserType
from dynatrace.pagination import PaginatedList


def test_list(dt: Dynatrace):
    audit_logs = dt.audit_logs.list()
    assert isinstance(audit_logs, PaginatedList)

    audit_logs_list = list(audit_logs)
    assert len(audit_logs_list) == 6

    first = audit_logs_list[0]
    assert isinstance(first, AuditLogEntry)
    assert first.log_id == "162100314800090003"
    assert first.event_type == EventType("DELETE")
    assert first.category == Category("CONFIG")
    assert first.entity_id == "builtin:alerting.profile (tenant): d89472d3-f9f4-420d-9398-768bb3351e85: test"
    assert first.environment_id == "eaa50379"
    assert first.user == "Dynatrace support user #649982176"
    assert first.user_type == UserType("USER_NAME")
    assert first.user_origin == "webui (xxx.xxx.xxx.xxx)"
    assert first.timestamp == datetime.utcfromtimestamp(1621003148800 / 1000)
    assert first.success


def test_get(dt: Dynatrace):
    audit_log = dt.audit_logs.get("162100314800090003")
    assert isinstance(audit_log, AuditLogEntry)
    assert audit_log.log_id == "162100314800090003"
    assert audit_log.event_type == EventType("DELETE")
    assert audit_log.category == Category("CONFIG")
    assert audit_log.entity_id == "builtin:alerting.profile (tenant): d89472d3-f9f4-420d-9398-768bb3351e85: test"
    assert audit_log.environment_id == "eaa50379"
    assert audit_log.user == "Dynatrace support user #649982176"
    assert audit_log.user_type == UserType("USER_NAME")
    assert audit_log.user_origin == "webui (xxx.xxx.xxx.xxx)"
    assert audit_log.timestamp == datetime.utcfromtimestamp(1621003148800 / 1000)
    assert audit_log.success
