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
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")


class AnsibleTowerNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.job_template_url: str = raw_element.get("jobTemplateURL")
        self.accept_any_certificate: bool = raw_element.get("acceptAnyCertificate")
        self.username: str = raw_element.get("username")
        self.password: str = raw_element.get("password")
        self.job_template_id: str = raw_element.get("jobTemplateID")
        self.custom_message: str = raw_element.get("customMessage")


class EmailNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.subject: str = raw_element.get("subject")
        self.body: str = raw_element.get("body")
        self.receivers: List[str] = raw_element.get("receivers")
        self.cc_receivers: List[str] = raw_element.get("ccReceivers")
        self.bcc_receivers: List[str] = raw_element.get("bccReceivers")


class HipChatNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.url: str = raw_element.get("url")
        self.message: str = raw_element.get("message")


class JiraNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.username: str = raw_element.get("username")
        self.password: str = raw_element.get("password")
        self.url: str = raw_element.get("url")
        self.project_key: str = raw_element.get("projectKey")
        self.issue_type: str = raw_element.get("issueType")
        self.summary: str = raw_element.get("summary")
        self.description: str = raw_element.get("description")


class OpsGenieNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.api_key: str = raw_element.get("apiKey")
        self.domain: str = raw_element.get("domain")
        self.message: str = raw_element.get("message")


class PagerDutyNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.account: str = raw_element.get("account")
        self.service_api_key: str = raw_element.get("serviceApiKey")
        self.service_name: str = raw_element.get("serviceName")


class ServiceNowNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.instance_name: str = raw_element.get("instanceName")
        self.url: str = raw_element.get("url")
        self.username: str = raw_element.get("username")
        self.password: str = raw_element.get("password")
        self.message: str = raw_element.get("message")
        self.send_incidents: bool = raw_element.get("sendIncidents")
        self.send_events: bool = raw_element.get("sendEvents")


class SlackNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.url: str = raw_element.get("url")
        self.channel: str = raw_element.get("channel")
        self.title: str = raw_element.get("title")


class TrelloNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.application_key: str = raw_element.get("applicationKey")
        self.authorization_token: str = raw_element.get("authorizationToken")
        self.board_id: str = raw_element.get("boardId")
        self.list_id: str = raw_element.get("listId")
        self.resolved_list_id: str = raw_element.get("resolvedListId")
        self.text: str = raw_element.get("text")
        self.description: str = raw_element.get("description")


class VictorOpsNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.api_key: str = raw_element.get("apiKey")
        self.routing_key: str = raw_element.get("routingKey")
        self.message: str = raw_element.get("message")


class HttpHeader(DynatraceObject):
    def _create_from_raw_data(self, raw_element):
        self.name: str = raw_element.get("name")
        self.value: str = raw_element.get("value")


class WebHookNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.url: str = raw_element.get("url")
        self.accept_any_certificate: bool = raw_element.get("acceptAnyCertificate")
        self.payload: str = raw_element.get("payload")
        self.headers: List[HttpHeader] = [HttpHeader(raw_element=header) for header in raw_element.get("headers", {})]
        self.notify_event_merges_enabled: bool = raw_element.get("notifyEventMergesEnabled")


class XMattersNotificationConfig(Notification):
    def _create_from_raw_data(self, raw_element):
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.notification_type: str = raw_element.get("type")
        self.alerting_profile: AlertingProfile = AlertingProfile(
            raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json()
        )
        self.active: bool = raw_element.get("active")
        self.url: str = raw_element.get("url")
        self.accept_any_certificate: bool = raw_element.get("acceptAnyCertificate")
        self.headers: List[HttpHeader] = [HttpHeader(raw_element=header) for header in raw_element.get("headers", {})]
        self.payload: str = raw_element.get("payload")


class NotificationConfigStub(DynatraceObject):
    def get_full_configuration(self) -> Notification:
        """
        Gets the full notification configuration for this stub.
        """
        response = self._http_client.make_request(f"/api/config/v1/notifications/{self.id}").json()
        if self.notification_type == "ANSIBLETOWER":
            notification = AnsibleTowerNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "EMAIL":
            notification = EmailNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "HIPCHAT":
            notification = HipChatNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "JIRA":
            notification = JiraNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "OPS_GENIE":
            notification = OpsGenieNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "PAGER_DUTY":
            notification = PagerDutyNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "SERVICE_NOW":
            notification = ServiceNowNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "SLACK":
            notification = SlackNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "TRELLO":
            notification = TrelloNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "VICTOROPS":
            notification = VictorOpsNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "WEBHOOK":
            notification = WebHookNotificationConfig(self._http_client, None, response)
        elif self.notification_type == "XMATTERS":
            notification = XMattersNotificationConfig(self._http_client, None, response)
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
