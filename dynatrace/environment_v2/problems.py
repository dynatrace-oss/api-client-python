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

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union, Dict, Any
from dynatrace.configuration_v1 import metag

from dynatrace.environment_v2.schemas import EntityType, ManagementZone
from dynatrace.http_client import HttpClient
from dynatrace.configuration_v1.metag import METag
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.pagination import PaginatedList
from dynatrace.utils import int64_to_datetime, timestamp_to_string

""" todo
---------------------------------------------
    comments
        - class / prototype
        - list/view/post/edit/delete
"""

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


class ProblemsServiceV2:
    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client


    def list(
        self,
        fields: Optional[str] = None,
        page_size: Optional[int] = None,
        time_from: Optional[Union[datetime, str]] = None,
        time_to: Optional[Union[datetime, str]] = None,
        problem_selector: Optional[str] = None,
        entity_selector: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> PaginatedList["Problem"]:
        """
        :return: A list of problems along with their details.
        """
        params = {
            "fields": fields,
            "pageSize": page_size,
            "from": timestamp_to_string(time_from),
            "to": timestamp_to_string(time_to),
            "problemSelector": problem_selector,
            "entitySelector": entity_selector,
            "sort": sort,
        }
        return PaginatedList(Problem, self.__http_client, "/api/v2/problems", target_params=params, list_item="problems")
    
    

    def get(self, problem_id: str, fields: Optional[str] = None) -> "Problem":
        response = self.__http_client.make_request(f"/api/v2/problems/{problem_id}")
        return Problem(raw_element=response)
    

    def close(self, problem_id: str, _message: Optional[str] = None):
        body = {"message": _message}
        return self.__http_client.make_request(f"api/v2/problems/{problem_id}/close", method="POST", data=body)



# todo - incomplete
class Problem(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.title: str = raw_element.get("title")
        self.problem_id: str = raw_element.get("problemId")
        self.display_id: str = raw_element.get("displayId")
        self.start_time: datetime = int64_to_datetime(raw_element.get("startTime"))
        self.end_time: datetime = int64_to_datetime(raw_element.get("endTime"))
        self.severity_level: SeverityLevel = SeverityLevel(raw_element.get("severityLevel"))
        self.impact_level: ImpactLevel = ImpactLevel(raw_element.get("impactLevel"))
        self.status: Status = Status(raw_element.get("status"))
        self.entity_tags: List[METag] = [METag(raw_element=tag) for tag in raw_element.get("entityTags", [])]
        self.management_zones: List[ManagementZone] = [ManagementZone(m) for m in raw_element.get("managementZones", [])]
