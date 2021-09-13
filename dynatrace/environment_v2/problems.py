"""
Copyright 2021 Dynatrace LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


from enum import Enum
from requests import Response
from datetime import datetime
from typing import Optional, Union, Dict, Any, List

from dynatrace.http_client import HttpClient
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.schemas import ManagementZone
from dynatrace.environment_v2.metrics import Unit
from dynatrace.environment_v2.monitored_entities import EntityStub
from dynatrace.environment_v2.custom_tags import METag
from dynatrace.configuration_v1.alerting_profiles import AlertingProfileStub
from dynatrace.pagination import PaginatedList
from dynatrace.utils import int64_to_datetime


class ProblemService:
    ENDPOINT = "/api/v2/problems"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        problem_selector: Optional[str] = None,
        entity_selector: Optional[str] = None,
        fields: Optional[str] = None,
        time_from: Optional[Union[datetime, str]] = None,
        time_to: Optional[Union[datetime, str]] = None,
        sort: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> PaginatedList["Problem"]:
        """Gets a list of Problems based on the given criteria.

        :return: a list of Problems along with their details.
        """
        params = {
            "problemSelector": problem_selector,
            "entitySelector": entity_selector,
            "fields": fields,
            "from": time_from,
            "to": time_to,
            "sort": sort,
            "pageSize": page_size,
        }
        return PaginatedList(target_class=Problem, http_client=self.__http_client, target_url=self.ENDPOINT, target_params=params, list_item="problems")

    def get(self, problem_id: str, fields: Optional[str] = None) -> "Problem":
        """Gets a Problem by specifying its id.

        :param problem_id: the ID of the Problem
        :return: a Problem along with its details
        """
        params = {"fields": fields}
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{problem_id}", params=params).json()
        return Problem(raw_element=response)

    def close(self, problem_id: str, message: str) -> "ProblemCloseResult":
        """Closes an open Problem leaving a closing message as comment

        :param message: message to leave as closing comment
        :param problem_id: the ID of the Problem
        :return: details of the closed problem result. Blank details if the problem was already closed.
        """
        params = {"message": message}
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{problem_id}/close", method="POST", params=params).json()
        return ProblemCloseResult(raw_element=response)

    def list_comments(self, problem_id: str, page_size: Optional[int] = 10) -> PaginatedList["Comment"]:
        """Gets a list of comments belonging to a given Problem.

        :param problem_id: the ID of the Problem
        :param page_size: the number of comments in a single response payload
        :return: a list of the Problem's comments
        """
        params = {"pageSize": page_size}
        return PaginatedList(
            target_class=Comment, http_client=self.__http_client, target_url=f"api/v2/{problem_id}/comments", target_params=params, list_item="comments"
        )

    def get_comment(self, problem_id: str, comment_id: str) -> "Comment":
        """Gets a specific Comment from a specific Problem

        :param problem_id: the ID of the Problem
        :param comment_id: the ID of the Comment
        :return: a Comment along with its details
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{problem_id}/comments/{comment_id}").json()
        return Comment(raw_element=response)

    def add_comment(self, problem_id: str, message: str, context: Optional[str] = None) -> Response:
        """Adds a new Comment on the specified Problem.

        :param problem_id: the ID of the Problem
        :param message: the text body of the Comment to add
        :param context: the optional context to attach to the Comment
        :return: HTTP Response
        """
        params = {"message": message, "context": context}
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{problem_id}/comments", params=params, method="POST")

    def update_comment(self, problem_id: str, comment_id: str, message: str, context: Optional[str] = None) -> Response:
        """Updates the specified Comment on a Problem.

        :param problem_id: the ID of the Problem
        :param comment_id: the ID of the Comment
        :param message: the new text body of the Comment to update
        :param context: the optional context to update on the Comment
        :return: HTTP Response
        """
        params = {"message": message, "context": context}
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{problem_id}/comments/{comment_id}", params=params, method="PUT")

    def delete_comment(self, problem_id: str, comment_id: str) -> Response:
        """Deletes the specified Comment from a Problem.

        :param problem_id: the ID of the Problem
        :param comment_id: the ID of the Comment
        :return: HTTP Response
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{problem_id}/comments/{comment_id}", method="DELETE")


class Problem(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        # required
        self.display_id: str = raw_element.get("displayId")
        self.problem_id: str = raw_element.get("problemId")
        self.title: str = raw_element.get("title")
        self.status: str = Status(raw_element.get("status"))
        self.severity_level: str = SeverityLevel(raw_element.get("severityLevel"))
        self.impact_level: str = ImpactLevel(raw_element.get("impactLevel"))
        self.start_time: datetime = int64_to_datetime(raw_element.get("startTime"))
        self.end_time: datetime = int64_to_datetime(raw_element.get("endTime")) if raw_element.get("endTime") != -1 else None

        # optional
        self.management_zones: Optional[List[ManagementZone]] = [ManagementZone(raw_element=m) for m in raw_element.get("managementZones", [])]
        self.affected_entities: Optional[List[EntityStub]] = [EntityStub(raw_element=e) for e in raw_element.get("affectedEntities", [])]
        self.recent_comments: Optional[CommentList] = CommentList(raw_element=raw_element.get("recentComments"))
        self.impacted_entities: Optional[List[EntityStub]] = [EntityStub(raw_element=e) for e in raw_element.get("impactedEntities", [])]
        self.linked_problem_info: Optional[LinkedProblem] = LinkedProblem(raw_element=raw_element.get("linkedProblemInfo"))
        self.root_cause_entity: Optional[EntityStub] = EntityStub(raw_element=raw_element["rootCauseEntity"]) if raw_element.get("rootCauseEntity") else None
        self.problem_filters: Optional[List[AlertingProfileStub]] = [AlertingProfileStub(raw_element=a) for a in raw_element.get("problemFilters", [])]
        self.evidence_details: Optional[EvidenceDetails] = EvidenceDetails(raw_element=raw_element.get("evidenceDetails"))
        self.impact_analysis: Optional[ImpactAnalysis] = ImpactAnalysis(raw_element=raw_element.get("impactAnalysis"))
        self.entity_tags: Optional[List[METag]] = [METag(raw_element=t) for t in raw_element.get("entityTags", [])]


class ProblemCloseResult(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.problem_id: str = raw_element.get("problemId")
        self.closing: bool = raw_element.get("closing")
        self.close_timestamp: datetime = int64_to_datetime(raw_element.get("closeTimestamp"))
        self.comment: Optional[Comment] = Comment(raw_element=raw_element.get("comment"))


class LinkedProblem(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.display_id: str = raw_element.get("displayId")
        self.problem_id: str = raw_element.get("problemId")


class CommentList(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.total_count: int = raw_element.get("totalCount")
        self.comments: Optional[List[Comment]] = [Comment(raw_element=c) for c in raw_element.get("comments", [])]


class Comment(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.created_at: datetime = int64_to_datetime(raw_element.get("createdAtTimestamp"))
        self.author: Optional[str] = raw_element.get("authorName")
        self.context: Optional[str] = raw_element.get("context")
        self.id: Optional[str] = raw_element.get("id")
        self.content: Optional[str] = raw_element.get("content")


class EvidenceDetails(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        raw_details = raw_element.get("details", [])
        self.total_count: int = raw_element.get("totalCount")
        self.details: Optional[List[Evidence]] = (
            [EventEvidence(raw_element=e) for e in raw_details if e.get("evidenceType") == EvidenceType.EVENT.value]
            + [MetricEvidence(raw_element=e) for e in raw_details if e.get("evidenceType") == EvidenceType.METRIC.value]
            + [TransactionalEvidence(raw_element=e) for e in raw_details if e.get("evidenceType") == EvidenceType.TRANSACTIONAL.value]
            + [MaintenanceWindowEvidence(raw_element=e) for e in raw_details if e.get("evidenceType") == EvidenceType.MAINTENANCE_WINDOW.value]
            + [AvailabilityEvidence(raw_element=e) for e in raw_details if e.get("evidenceType") == EvidenceType.AVAILABILITY.value]
        )


class Evidence(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.evidence_type: EvidenceType = EvidenceType(raw_element.get("evidenceType"))
        self.display_name: str = raw_element.get("displayName")
        self.entity: EntityStub = EntityStub(raw_element=raw_element.get("entity"))
        self.root_cause_relevant: bool = raw_element.get("rootCauseRelevant")
        self.start_time: datetime = int64_to_datetime(raw_element.get("startTime"))
        self.grouping_entity: Optional[EntityStub] = EntityStub(raw_element=raw_element.get("groupingEntity"))


class EventEvidence(Evidence):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.event_id: Optional[str] = raw_element.get("eventId")
        self.event_type: Optional[str] = raw_element.get("eventType")


class TransactionalEvidence(Evidence):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value_before_change_point: Optional[float] = raw_element.get("valueBeforeChangePoint")
        self.value_after_change_point: Optional[float] = raw_element.get("valueAfterChangePoint")
        self.end_time: Optional[datetime] = int64_to_datetime(raw_element.get("endTime"))
        self.unit: Optional[Unit] = Unit(raw_element.get("unit"))


class MetricEvidence(Evidence):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.value_before_change_point: Optional[float] = raw_element.get("valueBeforeChangePoint")
        self.value_after_change_point: Optional[float] = raw_element.get("valueAfterChangePoint")
        self.end_time: Optional[datetime] = int64_to_datetime(raw_element.get("endTime"))
        self.unit: Optional[Unit] = Unit(raw_element.get("unit"))
        self.metric_id: Optional[str] = raw_element.get("metricId")


class AvailabilityEvidence(Evidence):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.end_time: Optional[datetime] = int64_to_datetime(raw_element.get("endTime"))


class MaintenanceWindowEvidence(Evidence):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        super()._create_from_raw_data(raw_element)
        self.maintenance_window_id: Optional[str] = raw_element.get("maintenanceWindowConfigId")
        self.end_time: Optional[datetime] = int64_to_datetime(raw_element.get("endTime"))


class ImpactAnalysis(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.impacts: List[Impact] = [Impact(raw_element=i) for i in raw_element.get("impacts", [])]


class Impact(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.impact_type: ImpactType = ImpactType(raw_element.get("impactType"))
        self.impacted_entity: EntityStub = EntityStub(raw_element=raw_element.get("impactedEntity"))
        self.estimated_affected_users: int = raw_element.get("estimatedAffectedUsers")


class SeverityLevel(Enum):
    AVAILABILITY = "AVAILABILITY"
    CUSTOM_ALERT = "CUSTOM_ALERT"
    ERROR = "ERROR"
    MONITORING_UNAVAILABLE = "MONITORING_UNAVAILABLE"
    PERFORMANCE = "PERFORMANCE"
    RESOURCE_CONTENTION = "RESOURCE_CONTENTION"


class ImpactLevel(Enum):
    APPLICATION = "APPLICATION"
    ENVIRONMENT = "ENVIRONMENT"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    SERVICES = "SERVICES"


class Status(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class EvidenceType(Enum):
    EVENT = "EVENT"
    METRIC = "METRIC"
    TRANSACTIONAL = "TRANSACTIONAL"
    MAINTENANCE_WINDOW = "MAINTENANCE_WINDOW"
    AVAILABILITY = "AVAILABILITY_EVIDENCE"


class ImpactType(Enum):
    SERVICE = "SERVICE"
    APPLICATION = "APPLICATION"
    MOBILE = "MOBILE"
    CUSTOM_APPLICATION = "CUSTOM_APPLICATION"
