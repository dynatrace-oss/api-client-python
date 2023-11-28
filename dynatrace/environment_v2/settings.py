from datetime import datetime
from dynatrace.dynatrace_object import DynatraceObject
from typing import List, Optional, Union, Dict, Any

from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList
import json
import logging
from http.client import HTTPConnection  # py3


class SettingService:
    ENDPOINT = "/api/v2/settings/objects"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client
    
    def list(self,schema_id: Optional[str] = None,
             scope: Optional[str] = None,external_ids: Optional[str] = None,
             fields: Optional[str] = None,
             filter:Optional[str] = None, sort:Optional[str] = None, page_size:Optional[str] = None) -> PaginatedList["DynatraceObject"]:
        """Lists settings

        :return: a list of settings with details
        """
        params = {
            "schemaIds": schema_id,
            "scope": scope,
            "fields": fields,
            "externalIds": external_ids,
            "filter": filter,
            "sort": sort,
            "pageSize": page_size,
        }
        return PaginatedList(Settings, self.__http_client, target_url=self.ENDPOINT, list_item="items", target_params=params)
    
    def post(self,external_id,object_id,schema_id,schema_version,scope, value,validate_only):
        
        params = {
            "validate_only": validate_only,
        }
        body =[ {
            "externalId" : external_id,
            "objectId": object_id,
            "schemaId": schema_id,
            "schemaVersion": schema_version,
            "scope": scope,
            "value" : value

        }]
   
        response = self.__http_client.make_request(self.ENDPOINT,params=body, method="POST",query_params=params).json()
        return response
    
    
    def get(self, object_id: str):
        """Gets parameters of specified settings object

        :param object_id: the ID of the network zone
        :return: a Settings object
        """
        response = self.__http_client.make_request(f"{self.ENDPOINT}/{object_id}").json()
        return Settings(raw_element=response)

    def update(self, object_id: str,  value):
        """Updates an existing network zone or creates a new one

        :param networkzone_id: the ID of the network zone, if none exists, will create
        :param alternate_zones: optional list of text body of alternative network zones
        :param description: optional text body for short description of network zone
        :return: HTTP response
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{object_id}", params=value, method="PUT")

    def delete(self, object_id: str):
        """Deletes the specified object

        :param object_id: the ID of the network zone
        :return: HTTP response
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{object_id}", method="DELETE")

class Settings(DynatraceObject):
    value = None
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        # Mandatory
        self.objectId: str = raw_element["objectId"]
        self.value: str = raw_element["value"]
    def to_json(self):
        return  self.value