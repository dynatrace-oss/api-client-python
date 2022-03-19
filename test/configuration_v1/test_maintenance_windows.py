from dynatrace import Dynatrace
from dynatrace.configuration_v1.maintenance_windows import (
    TagCombination,
    MonitoredEntityFilter,
    Scope,
    Recurrence,
    Schedule,
    MaintenanceWindow,
    MaintenanceWindowStub,
)
from dynatrace.environment_v2.custom_tags import METag, TagContext
from dynatrace.pagination import PaginatedList

ID = "b6376a12-0b82-4069-9a41-0e55ef9a1f44"
NAME = "Example Window"


def test_list(dt: Dynatrace):
    mw = dt.maintenance_windows.list()
    assert isinstance(mw, PaginatedList)

    list_mw = list(mw)
    assert len(list_mw) == 3

    first = list_mw[0]
    assert isinstance(first, MaintenanceWindowStub)

    assert first.id == ID
    assert first.name == NAME


def test_get(dt: Dynatrace):
    mw = dt.maintenance_windows.get(profile_id=ID)

    # type checks
    assert isinstance(mw, MaintenanceWindow)
    assert isinstance(mw.id, str)
    assert isinstance(mw.name, str)
    assert isinstance(mw.description, str)
    assert isinstance(mw.type, str)
    assert isinstance(mw.suppression, str)
    assert isinstance(mw.suppress_synthetic_monitors_execution, bool)
    assert isinstance(mw.scope, Scope)
    assert isinstance(mw.schedule, Schedule)

    assert all(isinstance(rule, MonitoredEntityFilter) for rule in mw.scope.matches)
    for rule in mw.scope.matches:
        assert isinstance(rule.type, str)
        assert isinstance(rule.mz_id, str)
        for t in rule.tags:
            assert isinstance(t, METag)
        assert isinstance(rule.tag_combination, TagCombination)

    # value checks
    assert mw.id == ID
    assert mw.name == NAME
    assert mw.description == "An example Maintenance window"
    assert mw.type == "UNPLANNED"
    assert mw.suppression == "DETECT_PROBLEMS_AND_ALERT"
    assert mw.suppress_synthetic_monitors_execution == True
    assert mw.scope.entities[0] == "HOST-0000000000123456"
    assert mw.scope.matches[0].type == "HOST"
    assert mw.scope.matches[0].mz_id == "-5283929364044076484"
    assert mw.scope.matches[0].tags[0].context == TagContext.AWS
    assert mw.scope.matches[0].tags[0].key == "testkey"
    assert mw.scope.matches[0].tags[0].value == "testvalue"
    assert mw.scope.matches[0].tag_combination == TagCombination.AND
    assert mw.schedule.recurrence_type == "ONCE"
    assert isinstance(mw.schedule.recurrence, Recurrence)
    assert mw.schedule.start_time == "2018-08-02 00:00"
    assert mw.schedule.end_time == "2021-02-27 00:00"
    assert mw.schedule.zone_id == "Europe/Vienna"
