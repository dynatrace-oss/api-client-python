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
from dynatrace.dynatrace_object import DynatraceObject
from typing import List, Optional, Union, Dict, Any

from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList



class ExtensionsServiceV2:
    ENDPOINT = "/api/v2/extensions"
    SCHEMA_ENDPOINT = "/api/v2/extensions/schemas"


    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client


    def list(self) -> PaginatedList["MinimalExtension"]:
        """ Lists all the extensions 2.0 available in your environment

        :return: a list of MinimalExtension objects
        """
        return PaginatedList(MinimalExtension, self.__http_client, target_url=self.ENDPOINT, list_item="extensions")


    def list_versions(self, extension_name: str) -> PaginatedList["MinimalExtension"]:
        """ Lists all the extensions 2.0 by specified name in your environment

        :param extension_name: the name of the extension 2.0

        :return: a list of MinimalExtension objects
        """
        return PaginatedList(MinimalExtension, self.__http_client, target_url=f"{self.ENDPOINT}/{extension_name}", list_item="extensions")


    def list_environment_config_events(self, extension_name: str) -> PaginatedList["ExtensionEventDTO"]:
        """ List of the latest extension environment configuration events

        :param extension_name: the name of the extension 2.0

        :return: a list of ExtensionEventDTO object
        """
        return PaginatedList(ExtensionEventDTO, self.__http_client, target_url=f"{self.ENDPOINT}/{extension_name}/environmentConfiguration/events", list_item="extensionEvents")


    def list_monitoring_config_events(self, extension_name: str, config_id: str) -> PaginatedList["ExtensionEventDTO"]:
        """ Gets the list of the events linked to specific monitoring configuration

        :param extension_name: the name of the extension 2.0
        :param config_id: The ID of the requested monitoring configuration.

        :return: a list of ExtensionEventDTO object
        """
        return PaginatedList(ExtensionEventDTO, self.__http_client, target_url=f"{self.ENDPOINT}/{extension_name}/monitoringConfigurations/{config_id}/events", list_item="extensionEvents")
        

    def get(self, extension_name: str, extension_version: str) -> "Extension":
        """ Gets details of specified version of the extension 2.0

        :param extension_name: the name of the requested extension 2.0
        :param extension_version: the version of the requested extension 2.0
    
        :return: a Extension class object
        """
        response = self.__http_client.make_request(f"{self.ENDPOINT}/{extension_name}/{extension_version}").json()
        return Extension(raw_element=response)
    

    def delete(self, extension_name: str, extension_version: str):
        """ Deletes the specified version of the extension 2.0

        :param extension_name: the name of the requested extension 2.0
        :param extension_version: the version of the requested extension 2.0

        :return: HTTP response
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{extension_name}/{extension_version}", method="DELETE")
    

    def get_environment_config(self, extension_name: str) -> "ExtensionEnvironmentConfigurationVersion":
        """ Gets the active environment configuration version of the specified extension 2.0

        :param extension_name: the name of the requested extension 2.0

        :return: ExtensionEnvironmentConfigurationVersion object
        """
        response = self.__http_client.make_request(f"{self.ENDPOINT}/{extension_name}/environmentConfiguration").json()
        return ExtensionEnvironmentConfigurationVersion(raw_element=response)


    def put_environment_config(self, extension_name: str, _version: str):
        """ Updates the active environment configuration version of the extension 2.0

        :param extension_name: the name of the requested extension 2.0
        :param _version: the change to be put in place and activated

        :return: HTTP response
        """
        params = {"version": _version}
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{extension_name}/environmentConfiguration", params=params, method="PUT")
    
    
    def delete_environment_config(self, extension_name: str):
        """ Deactivates the environment configuration of the specified extension 2.0

        :param extension_name: the name of the requested extension 2.0 to deactivate

        :return: HTTP response
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{extension_name}/environmentConfiguration", method="DELETE")


class Extension(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.version: str = raw_element.get("version")
        self.extension_name: str = raw_element.get("extensionName")
        self.min_dynatrace_version: str = raw_element.get("minDynatraceVersion")
        self.file_hash: str = raw_element.get("fileHash")
        self.author: AuthorDTO = AuthorDTO(raw_element=raw_element.get("author"))
        self.data_sources: List[str] = raw_element.get("dataSources")
        self.variables: List[str] = raw_element.get("variables")
        self.feature_sets: List[str] = raw_element.get("featureSets")


class AuthorDTO(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.name: str = raw_element.get("name")


class ExtensionEventDTO(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.timestamp: str = raw_element.get("timestamp")
        self.severity: str = raw_element.get("severity")
        self.message: str = raw_element.get("message")


class ExtensionEnvironmentConfigurationVersion(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.version: str = raw_element.get("version")


class MinimalExtension(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.version: str = raw_element.get("version")
        self.extension_name: str = raw_element.get("extensionName")
    
    def list_versions(self):
        return self.version