from dynatrace import Dynatrace
from dynatrace.configuration_v1.notifications import NotificationConfigStub, NotificationType, ServiceNowNotificationConfig
from dynatrace.pagination import PaginatedList

ID = "0d06c889-4cea-4b45-aefa-a277790e784d"
NAME = "Service Now Example"
TYPE = NotificationType.SERVICE_NOW


def test_list(dt: Dynatrace):
    notifications = dt.notifications.list()
    assert isinstance(notifications, PaginatedList)

    list_notifications = list(notifications)
    assert len(list_notifications) == 4

    first = list_notifications[0]
    assert isinstance(first, NotificationConfigStub)

    assert first.id == ID
    assert first.name == NAME
    assert first.type == TYPE


def test_get_full_configuration(dt: Dynatrace):
    notifications = dt.notifications.list()
    list_notifications = list(notifications)
    first = list_notifications[0]

    full = first.get_full_configuration()

    # type checks
    assert isinstance(full, ServiceNowNotificationConfig)
    assert isinstance(full.name, str)
    assert isinstance(full.id, str)
    assert isinstance(full.type, NotificationType)
    assert isinstance(full.alerting_profile, str)
    assert isinstance(full.url, type(None))
    assert isinstance(full.username, str)
    assert isinstance(full.password, type(None))
    assert isinstance(full.message, str)
    assert isinstance(full.send_incidents, bool)
    assert isinstance(full.send_events, bool)

    # value checks
    assert full.id == ID
    assert full.name == NAME
    assert full.type == TYPE
    assert full.alerting_profile == "7693d108-fda9-3529-8ca3-55e9269b6097"
    assert full.active == True
    assert full.instance_name == "dev63549"
    assert full.url == None
    assert full.message == "{State} {ProblemID} {ProblemImpact} {ProblemSeverity}"
    assert full.send_incidents == True
    assert full.send_events == False
