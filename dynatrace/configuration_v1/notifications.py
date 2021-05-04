from typing import List
from requests import Response

from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.configuration_v1.alerting_profiles import AlertingProfile
from dynatrace.http_client import HttpClient


class Notification(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json())
        self.active: bool = raw_element.get("active")


class EmailNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json())
        self.active: bool = raw_element.get("active")
        self.subject: str = raw_element.get("subject")
        self.body: str = raw_element.get("body")
        self.receivers: List[str] = raw_element.get("receivers")
        self.cc_receivers: List[str] = raw_element.get("ccReceivers")
        self.bcc_receivers: List[str] = raw_element.get("bccReceivers")

class SlackNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json())
        self.active: bool = raw_element.get("active")
        self.url: str = raw_element.get("url")
        self.channel: str = raw_element.get("channel")
        self.title: str = raw_element.get("title")

class HttpHeader(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.name: str = raw_element.get("name")
        self.value: str = raw_element.get("value")

class WebHookNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json())
        self.active: bool = raw_element.get("active")
        self.url: str = raw_element.get("url")
        self.accept_any_certificate: bool = raw_element.get("acceptAnyCertificate")
        self.payload: str = raw_element.get("payload")
        self.headers: List[HttpHeader] = [HttpHeader(raw_element=header) for header in raw_element.get("headers", {})]
        self.notify_event_merges_enabled: bool = raw_element.get("notifyEventMergesEnabled")


class NotificationConfigStub(DynatraceObject):
    def get_full_configuration(self) -> Notification:
        """
        Gets the full notification configuration for this stub.
        """
        response = self._http_client.make_request(f"/api/config/v1/notifications/{self.id}").json()
        if self.notification_type == "EMAIL":
            notification = EmailNotificationConfig(self._http_client, None, response)
        if self.notification_type == "SLACK":
            notification = SlackNotificationConfig(self._http_client, None, response)
        if self.notification_type == "WEBHOOK":
            notification = WebHookNotificationConfig(self._http_client, None, response)
        else:
            notification = Notification(self._http_client, None, response)
        return notification

    def delete(self) -> Response:
        """
        Delete the notification for this stub.
        """
        return self._http_client.make_request(f"/api/config/v1/notifications/{self.id}", method="DELETE")

    def _create_from_raw_data(self, raw_element):
        self.id = raw_element.get("id")
        self.name = raw_element.get("name")
        self.description = raw_element.get("description")
        self.notification_type = raw_element.get("type")


class NotificationService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList[NotificationConfigStub]:
        """
        Lists all alerting profiles in the environmemt. No configurable parameters.
        """
        return PaginatedList(NotificationConfigStub, self.__http_client, f"/api/config/v1/notifications", list_item="values")

    def delete(self, notification_id: str) -> Response:
        """
        Delete the notification with the specified id.
        """
        return self.__http_client.make_request(f"/api/config/v1/notifications/{notification_id}", method="DELETE")
