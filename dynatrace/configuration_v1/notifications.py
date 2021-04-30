from typing import List, Optional
from requests import Response

from dynatrace.pagination import PaginatedList
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.entity import EntityShortRepresentation
from dynatrace.configuration_v1.alerting_profiles import AlertingProfile
from dynatrace.http_client import HttpClient

class Notification(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def notification_type(self) -> str:
        return self._notification_type

    @property
    def alerting_profile(self) -> AlertingProfile:
        return self._alerting_profile

    @property
    def active(self) -> bool:
        return self._active

    def _create_from_raw_data(self, raw_element):
        self._id = raw_element.get("id")
        self._name = raw_element.get("name")
        self._notification_type = raw_element.get("type")
        self._alerting_profile = AlertingProfile(raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json())
        self._active = raw_element.get("active")
        
class EmailNotificationConfig(Notification):  
    @property
    def subject(self) -> str:
        return self._subject

    @property
    def body(self) -> str:
        return self._body

    @property
    def receivers(self) -> List[str]:
        return self._receivers

    @property
    def cc_receivers(self) -> List[str]:
        return self._cc_receivers

    @property
    def bcc_receivers(self) -> List[str]:
        return self._bcc_receivers
    
    def _create_from_raw_data(self, raw_element):
        self._id = raw_element.get("id")
        self._name = raw_element.get("name")
        self._notification_type = raw_element.get("type")
        self._alerting_profile = AlertingProfile(raw_element=self._http_client.make_request(f"/api/config/v1/alertingProfiles/{raw_element.get('alertingProfile')}").json())
        self._active = raw_element.get("active")
        self._subject = raw_element.get("subject")
        self._body = raw_element.get("body")
        self._receivers = raw_element.get("receivers")
        self._cc_receivers = raw_element.get("ccReceivers")
        self._bcc_receivers = raw_element.get("bccReceivers")

class NotificationStub(DynatraceObject):
    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def notification_type(self) -> str:
        return self._notification_type

    def get_full_configuration(self) -> Notification:
        """
        Gets the full notification configuration for this stub.
        """
        response = self._http_client.make_request(f"/api/config/v1/notifications/{self.id}").json()
        if self._notification_type == "EMAIL":
            notification = EmailNotificationConfig(self._http_client, None, response)
        else:
            notification = Notification(self._http_client, None, response)
        return notification

    def delete(self) -> Response:
        """
        Delete the notification for this stub.
        """
        return self._http_client.make_request(f"/api/config/v1/notifications/{self.id}", method="DELETE")

    def _create_from_raw_data(self, raw_element):
        self._id = raw_element.get("id")
        self._name = raw_element.get("name")
        self._description = raw_element.get("description")
        self._notification_type = raw_element.get("type")

class NotificationService:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self) -> PaginatedList[NotificationStub]:
        """
        Lists all alerting profiles in the environmemt. No configurable parameters.
        """
        return PaginatedList(NotificationStub, self.__http_client, f"/api/config/v1/notifications", list_item="values")

    def delete(self, notification_id: str) -> Response:
        """
        Delete the notification with the specified id.
        """
        return self.__http_client.make_request(f"/api/config/v1/notifications/{notification_id}", method="DELETE")