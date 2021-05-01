from dynatrace import Dynatrace
from dynatrace.configuration_v1.alerting_profiles import AlertingProfileStub, AlertingProfile, AlertingProfileSeverityRule
from dynatrace.pagination import PaginatedList


def test_list(dt: Dynatrace):
    alert_profiles = dt.alerting_profiles.list()
    assert isinstance(alert_profiles, PaginatedList)

    list_alert_profiles = list(alert_profiles)
    assert len(list_alert_profiles) == 6

    first = list_alert_profiles[0]
    assert isinstance(first, AlertingProfileStub)

    assert first.id == "b1f379d9-98b4-4efe-be38-0289609c9295"
    assert first.name == "deployment_change_autoremediation"


def test_get_full_configuration(dt: Dynatrace):
    alert_profiles = dt.alerting_profiles.list()
    list_alert_profiles = list(alert_profiles)
    first = list_alert_profiles[0]

    full = first.get_full_configuration()
    assert isinstance(full, AlertingProfile)
    assert full.id == "b1f379d9-98b4-4efe-be38-0289609c9295"
    assert full.display_name == "deployment_change_autoremediation"
    assert isinstance(full.rules, list)
    assert isinstance(full.rules[0], AlertingProfileSeverityRule)
