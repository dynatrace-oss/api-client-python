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

from requests.models import Response

from dynatrace.http_client import HttpClient
from dynatrace.configuration_v1.metag import METag
from dynatrace.pagination import PaginatedList
from dynatrace.utils import timestamp_to_string


class CustomTagService:
    ENDPOINT = "/api/v2/tags"


    def __init__(self, http_client: HttpClient) -> None:
        self.__http_client = http_client
    

    def list(self, entity_selector: str, time_from: Optional[Union[datetime, str]] = None, time_to: Optional[Union[datetime, str]] = None) -> PaginatedList["METag"]:
        """ 
        Returns a list of custom tags
        :param entitySelector: specifies entities where you want to read tags

        :return: a list of METag objects 
        """
        params = {
            "entitySelector": entity_selector,
            "from": timestamp_to_string(time_from),
            "to": timestamp_to_string(time_to)
        }

        return PaginatedList(METag, self.__http_client, target_url=self.ENDPOINT, target_params=params, list_item="tags")


    def post(
        self,
        entity_selector: str,
        tags: List[Dict[str, Any]],
        time_from: Optional[Union[datetime, str]] = None,
        time_to: Optional[Union[datetime, str]] = None
    ) -> None:
        """
        Adds custom tags to the specified entities
        :param entitySelector: specifies entities where you want to read tags
        :param tags: list of Tag objects Tag = { key, value(optional)}

        :return: HTTP Response
        """
        params = {
            "entitySelector": entity_selector,
            "body": {"tags": tags},
            "from": timestamp_to_string(time_from),
            "to": timestamp_to_string(time_to)
        }
        return self.__http_client.make_request(path=f"{self.ENDPOINT}", params=params, method="POST")
    


    def delete(
        self,
        key: str,
        entity_selector: str,
        value: Optional[str] = None,
        delete_all_with_key: Optional[bool] = None,
        time_from: Optional[Union[datetime, str]] = None,
        time_to: Optional[Union[datetime, str]] = None
    ) -> Response:
        """
        Deletes the specified tag from the specified entities

        :param key: the tag to be deleted
        :param entity_selector: specifies entities where you want to delete tags
        :param deleteallwithkey: boolean to delete all optional
        :param value: optional

        :return: HTTP response
        """
        params = {
            "key": key,
            "entitySelector": entity_selector,
            "deleteAllWithKey": delete_all_with_key,
            "value": value
        }
        return self.__http_client.make_request(path=f"{self.ENDPOINT}", params=params, method="DELETE")