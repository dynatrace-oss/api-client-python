from datetime import datetime
from typing import List, Optional

from dynatrace.dynatrace_object import DynatraceObject

SYNTHETIC_EVENT_TYPE_OUTAGE = "testOutage"
SYNTHETIC_EVENT_TYPE_SLOWDOWN = "testSlowdown"


class ThirdPartySyntheticTests(DynatraceObject):
    def __init__(
        self,
        http_client,
        synthetic_engine_name: str,
        message_timestamp: datetime,
        locations: List["ThirdPartySyntheticLocation"],
        tests: List["ThirdPartySyntheticMonitor"],
        test_results: Optional[List["ThirdPartySyntheticResult"]] = None,
        synthetic_engine_icon_url: Optional[str] = None,
    ):

        raw_element = {
            "syntheticEngineName": synthetic_engine_name,
            "syntheticEngineIconUrl": synthetic_engine_icon_url,
            "messageTimestamp": int(message_timestamp.timestamp() * 1000),
            "locations": [location._raw_element for location in locations],
            "tests": [test._raw_element for test in tests],
            "testResults": [test_result._raw_element for test_result in test_results] if test_results else None,
        }
        super().__init__(http_client, None, raw_element)

    def post(self):
        return self._http_client.make_request(f"/api/v1/synthetic/ext/tests", params=self._raw_element, method="POST")


class ThirdPartySyntheticLocation(DynatraceObject):
    def __init__(self, http_client, location_id: str, name: str, ip: Optional[str] = None):

        raw_element = {"id": location_id, "name": name, "ip": ip}
        super().__init__(http_client, None, raw_element)


class ThirdPartySyntheticMonitor(DynatraceObject):
    def __init__(
        self,
        http_client,
        test_id: str,
        title: str,
        locations: List["SyntheticTestLocation"],
        schedule_interval_in_seconds: int,
        description: Optional[str] = None,
        test_setup: Optional[str] = None,
        expiration_timestamp: Optional[int] = None,
        drilldown_link: Optional[str] = None,
        edit_link: Optional[str] = None,
        deleted: Optional[bool] = None,
        steps: Optional[List["SyntheticTestStep"]] = None,
        no_data_timeout: Optional[int] = None,
    ):

        raw_element = {
            "id": test_id,
            "title": title,
            "description": description,
            "testSetup": test_setup,
            "expirationTimestamp": expiration_timestamp,
            "drilldownLink": drilldown_link,
            "editLink": edit_link,
            "deleted": deleted,
            "locations": [location._raw_element for location in locations],
            "steps": [step._raw_element for step in steps] if steps else None,
            "scheduleIntervalInSeconds": schedule_interval_in_seconds,
            "noDataTimeout": no_data_timeout,
        }
        super().__init__(http_client, None, raw_element)


class SyntheticTestLocation(DynatraceObject):
    def __init__(self, http_client, location_id: str, enabled: Optional[bool] = None):

        raw_element = {"id": location_id, "enabled": enabled}
        super().__init__(http_client, None, raw_element)


class SyntheticTestStep(DynatraceObject):
    def __init__(self, http_client, step_id: int, title: str):
        self.step_id = step_id
        self.title = title

        raw_element = {"id": step_id, "title": title}
        super().__init__(http_client, None, raw_element)


class ThirdPartySyntheticResult(DynatraceObject):
    def __init__(
        self,
        http_client,
        test_id: str,
        total_step_count: int,
        location_results: List["ThirdPartySyntheticLocationTestResult"],
        schedule_interval_in_seconds: Optional[int] = None,
    ):

        raw_element = {
            "id": test_id,
            "scheduleIntervalInSeconds": schedule_interval_in_seconds,
            "totalStepCount": total_step_count,
            "locationResults": [location_result._raw_element for location_result in location_results],
        }
        super().__init__(http_client, None, raw_element)


class ThirdPartySyntheticLocationTestResult(DynatraceObject):
    def __init__(
        self,
        http_client,
        location_id: str,
        start_timestamp: datetime,
        success: bool,
        success_rate: Optional[float] = None,
        response_time_millis: Optional[int] = None,
        step_results: Optional[List["SyntheticMonitorStepResult"]] = None,
    ):

        raw_element = {
            "id": location_id,
            "startTimestamp": int(start_timestamp.timestamp() * 1000),
            "successRate": success_rate,
            "success": success,
            "responseTimeMillis": response_time_millis,
            "stepResults": [step_result._raw_element for step_result in step_results] if step_results else None,
        }
        super().__init__(http_client, None, raw_element)


class SyntheticMonitorStepResult(DynatraceObject):
    def __init__(
        self,
        http_client,
        step_id: int,
        start_timestamp: datetime,
        response_time_millis: Optional[int] = None,
        error: Optional["SyntheticMonitorError"] = None,
    ):

        raw_element = {
            "id": step_id,
            "startTimestamp": int(start_timestamp.timestamp() * 1000),
            "responseTimeMillis": response_time_millis,
            "error": error._raw_element if error else None,
        }
        super().__init__(http_client, None, raw_element)


class SyntheticMonitorError(DynatraceObject):
    def __init__(self, http_client, code: int, message: str):

        raw_element = {"code": code, "message": message}
        super().__init__(http_client, None, raw_element)


class ThirdPartySyntheticEvents(DynatraceObject):
    def __init__(
        self,
        http_client,
        synthetic_engine_name: str,
        open_events: Optional[List["ThirdPartyEventOpenNotification"]],
        resolved_events: Optional[List["ThirdPartyEventResolvedNotification"]],
    ):

        raw_element = {
            "syntheticEngineName": synthetic_engine_name,
            "open": [open_event._raw_element for open_event in open_events] if open_events else None,
            "resolved": [resolved_event._raw_element for resolved_event in resolved_events] if resolved_events else None,
        }
        super().__init__(http_client, None, raw_element)

    def post(self):
        return self._http_client.make_request(f"/api/v1/synthetic/ext/events", params=self._raw_element, method="POST")


class ThirdPartyEventOpenNotification(DynatraceObject):
    def __init__(
        self,
        http_client,
        test_id: str,
        event_id: str,
        name: str,
        event_type: str,
        reason: str,
        start_timestamp: datetime,
        location_ids: List[str],
    ):

        raw_element = {
            "testId": test_id,
            "eventId": event_id,
            "name": name,
            "eventType": event_type,
            "reason": reason,
            "startTimestamp": int(start_timestamp.timestamp() * 1000),
            "locationIds": location_ids,
        }
        super().__init__(http_client, None, raw_element)


class ThirdPartyEventResolvedNotification(DynatraceObject):
    def __init__(self, http_client, test_id: str, event_id: str, end_timestamp: datetime):

        raw_element = {"testId": test_id, "eventId": event_id, "endTimestamp": int(end_timestamp.timestamp() * 1000)}
        super().__init__(http_client, None, raw_element)
