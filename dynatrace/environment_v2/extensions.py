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

from dynatrace.dynatrace_object import DynatraceObject
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList


class ExtensionsServiceV2:
    ENDPOINT = "/api/v2/extensions"
    SCHEMA_ENDPOINT = "/api/v2/extensions/schemas"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self, name: Optional[str] = None) -> PaginatedList["MinimalExtension"]:
        """Lists all the extensions 2.0 available in your environment"""
        params = {"name": name}
        return PaginatedList(MinimalExtension, self.__http_client, target_url=self.ENDPOINT, list_item="extensions", target_params=params)

    def list_versions(self, extension_name: str) -> PaginatedList["MinimalExtension"]:
        """Lists all the extensions 2.0 by specified name in your environment

        :param extension_name: the name of the extension 2.0
        """
        return PaginatedList(MinimalExtension, self.__http_client, target_url=f"{self.ENDPOINT}/{extension_name}", list_item="extensions")

    def list_environment_config_events(self, extension_name: str) -> PaginatedList["ExtensionEventDTO"]:
        """List of the latest extension environment configuration events

        :param extension_name: the name of the extension 2.0

        :return: a list of ExtensionEventDTO object
        """
        return PaginatedList(
            ExtensionEventDTO, self.__http_client, target_url=f"{self.ENDPOINT}/{extension_name}/environmentConfiguration/events", list_item="extensionEvents"
        )

    def list_monitoring_config_events(self, extension_name: str, config_id: str) -> PaginatedList["ExtensionEventDTO"]:
        """Gets the list of the events linked to specific monitoring configuration

        :param extension_name: the name of the extension 2.0
        :param config_id: The ID of the requested monitoring configuration.

        :return: a list of ExtensionEventDTO object
        """
        return PaginatedList(
            ExtensionEventDTO,
            self.__http_client,
            target_url=f"{self.ENDPOINT}/{extension_name}/monitoringConfigurations/{config_id}/events",
            list_item="extensionEvents",
        )

    def get(self, extension_name: str, extension_version: str) -> "Extension":
        """Gets details of specified version of the extension 2.0

        :param extension_name: the name of the requested extension 2.0
        :param extension_version: the version of the requested extension 2.0

        :return: a Extension class object
        """
        response = self.__http_client.make_request(f"{self.ENDPOINT}/{extension_name}/{extension_version}").json()
        return Extension(raw_element=response)

    def post(self, zip_file_path: Union[str, Path], validate_only: Optional[bool] = False):
        """Post the specified version of the extension 2.0

        :param zip_file_path: path to zipped extension 2.0
        :param validate_only: optionally run validation but do not persist the extension even if validation was successful

        :return: newly created Extension class object
        """
        params = {"validateOnly": validate_only}
        file = Path(zip_file_path)
        with open(file, "rb") as f:
            response = self.__http_client.make_request(f"{self.ENDPOINT}", params=params, method="POST", files={"file": f}).json()
            return Extension(raw_element=response)

    def delete(self, extension_name: str, extension_version: str):
        """Deletes the specified version of the extension 2.0

        :param extension_name: the name of the requested extension 2.0
        :param extension_version: the version of the requested extension 2.0

        :return: HTTP response
        """
        return self.__http_client.make_request(f"{self.ENDPOINT}/{extension_name}/{extension_version}", method="DELETE")

    def get_environment_config(self, extension_name: str) -> "ExtensionEnvironmentConfigurationVersion":
        """Gets the active environment configuration version of the specified extension 2.0

        :param extension_name: the name of the requested extension 2.0

        :return: ExtensionEnvironmentConfigurationVersion object
        """
        response = self.__http_client.make_request(f"{self.ENDPOINT}/{extension_name}/environmentConfiguration").json()
        return ExtensionEnvironmentConfigurationVersion(raw_element=response)

    def put_environment_config(self, extension_name: str, extension_version: str):
        """Updates an existing active environment configuration version of the extension 2.0

        :param extension_name: the name of the requested extension 2.0
        :param extension_version: the version of the requested extension 2.0

        :return: HTTP response
        """
        params = {"version": extension_version}
        return self.__http_client.make_request(f"{self.ENDPOINT}/{extension_name}/environmentConfiguration", method="PUT", params=params)

    def delete_environment_config(self, extension_name: str):
        """Deactivates the environment configuration of the specified extension 2.0

        :param extension_name: the name of the requested extension 2.0 to deactivate

        :return: HTTP response
        """
        return self.__http_client.make_request(f"{self.ENDPOINT}/{extension_name}/environmentConfiguration", method="DELETE")

    def list_schemas(self, schema_version: str) -> "SchemaFiles":
        response = self.__http_client.make_request(f"{self.SCHEMA_ENDPOINT}/{schema_version}")
        return SchemaFiles(raw_element=response.json())

    def get_schema_file(self, schema_version: str, file_name: str) -> Dict[str, Any]:
        return self.__http_client.make_request(f"{self.SCHEMA_ENDPOINT}/{schema_version}/{file_name}").json()

    def post_monitoring_configurations(self, extension_name: str, configurations: List["MonitoringConfigurationDto"]) -> List:
        params = [c.to_json() for c in configurations]
        response = self.__http_client.make_request(f"{self.ENDPOINT}/{extension_name}/monitoringConfigurations", params=params, method="POST")
        return response.json()


class SchemaFiles(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.files: List[str] = raw_element.get("files", [])


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

    def to_json(self) -> Dict[str, Any]:
        """Translates an ExtensionEnvironmentConfigurationVersion to a JSON dict."""
        return {"version": self.version}

    def put(self, extension_name: str):
        """Updates an existing extension environment config's version in Dynatrace

        :param extension_name: the name of the extension required for making the API call
        """
        return self._http_client.make_request(f"{ExtensionsServiceV2.ENDPOINT}/{extension_name}/environmentConfiguration", params=self.to_json(), method="PUT")


class MinimalExtension(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.version: str = raw_element.get("version")
        self.extension_name: str = raw_element.get("extensionName")

    def list_version(self) -> str:
        """Class method for obtaining extension2.0 version"""
        return self.version

    def get_environment_config(self) -> "ExtensionEnvironmentConfigurationVersion":
        """Gets the active environment configuration version of the specified extension 2.0

        :return: ExtensionEnvironmentConfigurationVersion object
        """
        response = self._http_client.make_request(f"{ExtensionsServiceV2.ENDPOINT}/{self.extension_name}/environmentConfiguration").json()
        return ExtensionEnvironmentConfigurationVersion(raw_element=response)

    def list_environment_config_events(self) -> PaginatedList["ExtensionEventDTO"]:
        """List of the latest extension environment configuration events

        :return: a list of ExtensionEventDTO object
        """
        return PaginatedList(
            ExtensionEventDTO,
            self._http_client,
            target_url=f"{ExtensionsServiceV2.ENDPOINT}/{self.extension_name}/environmentConfiguration/events",
            list_item="extensionEvents",
        )

    def list_monitoring_config_events(self, config_id) -> PaginatedList["ExtensionEventDTO"]:
        """Gets the list of the events linked to specific monitoring configuration

        :param config_id: The ID of the requested monitoring configuration.

        :return: a list of ExtensionEventDTO object
        """
        return PaginatedList(
            ExtensionEventDTO,
            self._http_client,
            target_url=f"{ExtensionsServiceV2.ENDPOINT}/{self.extension_name}/monitoringConfigurations/{config_id}/events",
            list_item="extensionEvents",
        )


class MonitoringConfigurationDto:
    def __init__(self, scope: str, configuration: Dict[str, Any]):
        self.scope = scope
        self.configuration = configuration

    def to_json(self):
        return {"scope": self.scope, "value": self.configuration}
