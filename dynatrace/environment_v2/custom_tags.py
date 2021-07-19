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
from typing import List, Optional, Union, Dict, Any

from dynatrace.environment_v2.schemas import EntityType, ManagementZone
from dynatrace.http_client import HttpClient
from dynatrace.configuration_v1.metag import METag
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.pagination import PaginatedList
from dynatrace.utils import timestamp_to_string


class CustomTagService:
    ENDPOINT = "/api/v2/tags"


    def __init__(self, http_client: HttpClient) -> None:
        self.__http_client = http_client
    

    def list(
        self,
        entity_selector: str,
        time_from: Optional[Union[datetime, str]] = None,
        time_to: Optional[Union[datetime, str]] = None,
    ) -> PaginatedList["METag"]:
        """ 
        Returns a list of custom tags
        :param entitySelector - specifies entities where you want to read tags

        :return: a list of METag objects 
        """
        params = {
            "entitySelector": entity_selector,
            "from": timestamp_to_string(time_from),
            "to": timestamp_to_string(time_to)
        }

        return PaginatedList(METag, self.__http_client, target_url=self.ENDPOINT, target_params=params, list_item="tags")

    
    
